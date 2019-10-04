import datetime
import re

import pandas as pd
from fylesdk import FyleSDK
from xero import Xero, auth
from xero.auth import PrivateCredentials

from apps.xero_workspace.models import XeroCredential, FyleCredential, CategoryMapping, EmployeeMapping, Workspace
from fyle_xero_integration_web_app.settings import FYLE_BASE_URL, FYLE_CLIENT_ID, FYLE_CLIENT_SECRET


def connect_xero_private(workspace_id):
    """
    Returns verified instance of Xero object that can invoke private API calls for a given workspace.
    :param workspace_id: Id of the Xero workspace
    :return: verified instance of Xero object
    """
    xero_credential = XeroCredential.objects.get(id=workspace_id)
    rsa_key_path = xero_credential.pem_file.path
    consumer_key = xero_credential.consumer_key

    with open(rsa_key_path) as keyfile:
        rsa_key = keyfile.read()

    credentials = PrivateCredentials(consumer_key, rsa_key)
    xero = Xero(credentials)
    return xero


def connect_to_xero(workspace_id):
    """ Returns verified instance of Xero object that can invoke private API calls.
    :param workspace_id: Id of the workspace containing rsa_key and consumer_key of Xero private application
    :return: verified instance of Xero object
    """
    xero_credential = XeroCredential.objects.get(workspace__id=workspace_id)
    consumer_key = xero_credential.consumer_key
    rsa_key = xero_credential.private_key
    credentials = auth.PrivateCredentials(consumer_key, rsa_key)
    xero = Xero(credentials)
    return xero


def connect_to_fyle(workspace_id):
    """
    Returns verified instance of Fyle object that can invoke API calls
    :param workspace_id:
    :return:
    """
    refresh_token = FyleCredential.objects.get(workspace__id=workspace_id).fyle_auth.refresh_token
    connection = FyleSDK(
        base_url=FYLE_BASE_URL,
        client_id=FYLE_CLIENT_ID,
        client_secret=FYLE_CLIENT_SECRET,
        refresh_token=refresh_token
    )
    return connection


def load_mapping(workspace_id, conn, xero):
    """
    Loads Fyle-Xero mappings into SQLite database
    :param xero: Xero connection object
    :param workspace_id:
    :param conn:
    :return:
    """
    # Get category-account mappings
    category_mapping_qs = CategoryMapping.objects.filter(workspace__id=workspace_id).values('category', 'sub_category',
                                                                                            'account_code')
    category_mappings_list = list(category_mapping_qs)
    df_category_mappings = pd.DataFrame(category_mappings_list)
    df_category_mappings.rename(
        columns={'category': 'CategoryName', 'sub_category': 'SubCategoryName', 'account_code': 'AccountCode'},
        inplace=True)
    df_category_mappings['AccountCode'] = df_category_mappings['AccountCode'].astype('int')
    df_category_mappings.to_sql('category_account', conn, if_exists='replace', index=False)

    # Get employee mappings
    employee_mapping_qs = EmployeeMapping.objects.filter(workspace__id=workspace_id).values('employee_email',
                                                                                            'contact_name')
    employee_mapping_list = list(employee_mapping_qs)
    df_employee_mappings = pd.DataFrame(employee_mapping_list)
    df_employee_mappings.rename(columns={'employee_email': 'EmployeeEmail', 'contact_name': 'ContactName'},
                                inplace=True)
    for name in df_employee_mappings['ContactName']:
        xero_contact_info = xero.contacts.filter(Name=name)
        df_employee_mappings['ContactID'] = xero_contact_info[0]['ContactID']
    df_employee_mappings.to_sql('employee_contact', conn, if_exists='replace', index=False)


def generate_invoice_request_data(conn):
    """ Returns the request data for creating Xero invoices
    :param conn: sqlite connection object
    :return request_data:
    """
    df_invoice = pd.read_sql_query(
        sql='select * from invoices', con=conn)

    #  For loop that iterates over invoice DateFrame and converts datetime in string to python datetime
    for i in range(len(df_invoice['Date'])):
        df_invoice['Date'][i] = datetime.datetime(*map(int, re.split(r'[^\d]', df_invoice['Date'][i])[:-1]))
        df_invoice['DueDate'][i] = datetime.datetime(*map(int, re.split(r'[^\d]', df_invoice['DueDate'][i])[:-1]))

    # Convert invoice DateFrame to invoice list
    request_data = df_invoice.to_dict(orient='records')

    #  For loop that iterates over invoice list and fetches the corresponding Line items
    for invoice in request_data:
        df_invoice_line_items = pd.read_sql_query(
            sql='select * from invoice_line_items where InvoiceNumber = "{}"'.format(invoice['InvoiceNumber']),
            con=conn)
        df_invoice_line_items.drop(columns='InvoiceNumber', inplace=True)
        invoice_line_items = df_invoice_line_items.to_dict(orient='records')
        invoice['LineItems'] = invoice_line_items
        invoice['Contact'] = {'ContactID': invoice['ContactID']}

    conn.close()
    return request_data


def create_invoice(data, xero):
    """ Makes an API call to create invoices in Xero
    :param data: Request data for the invoice API
    :param xero: Xero connection object
    :return response: response data from Xero API
    """
    response = xero.invoices.put(data)
    return response


def transform(conn, workspace_id):
    """
    Transforms the collected fyle and mapping data into Xero API consumption
    :param conn:
    :param workspace_id:
    :return:
    """
    qry = Workspace.objects.get(id=workspace_id).transform_sql
    cur = conn.cursor()
    cur.executescript(qry)
    cur.close()
    conn.commit()
