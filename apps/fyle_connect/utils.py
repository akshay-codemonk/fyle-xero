import json
import pandas as pd
import numpy as np
import requests

from fyle_xero_integration_web_app import settings


class FyleOAuth2():

    def __init__(self):
        """
        initialize from settings
        """
        self.client_id = settings.FYLE_CLIENT_ID
        self.client_secret = settings.FYLE_CLIENT_SECRET
        self.authorise_uri = settings.FYLE_AUTHORISE_URI
        self.callback_uri = settings.FYLE_CALLBACK_URI
        self.token_url = settings.FYLE_TOKEN_URI

    def authorise(self, state):
        """
        Initiates the Fyle OAuth2.0 Authorise flow
        :param state:
        :return:
        """
        authorisation_redirect_url = self.authorise_uri + '?response_type=code&client_id=' + self.client_id + \
                                     '&redirect_uri=' + self.callback_uri + '&scope=read' + '&state=' + state
        return authorisation_redirect_url

    def get_tokens(self, authorization_code):
        """
        Exchange the authorisation_code for access and refresh tokens
        :param authorization_code:
        :return dict containing access_token, refresh_token and expiry:
        """
        # authorization_code = raw_input('code: ')

        data = {'grant_type': 'authorization_code', 'client_id': self.client_id, 'client_secret': self.client_secret,
                'code': authorization_code}
        access_token_response = requests.post(self.token_url, data=data, verify=False, allow_redirects=False)

        tokens = json.loads(access_token_response.text)

        return tokens


def extract_fyle(connection, conn):
    """
    extracts data from fyle and store in SQLite database
    :param connection:
    :param conn: SQLite connection object
    :return:
    """

    employees = connection.Employees.get_all()
    settlements = list(filter(lambda settlement: not settlement['exported'], connection.Settlements.get_all()))
    if settlements:
        df_settlements = pd.DataFrame(settlements)
        reimbursements = list(filter(lambda reimbursement: reimbursement['settlement_id'] in list(df_settlements['id']),
                                     connection.Reimbursements.get_all()))
        df_reimbursements = pd.DataFrame(reimbursements)
        expenses = list(
            filter(lambda expense: expense['settlement_id'] in list(df_settlements['id']) and expense['reimbursable'],
                   connection.Expenses.get_all()))
        df_employees = pd.DataFrame(employees)
        df_employees['annual_mileage_of_user_before_joining_fyle'] = df_employees[
            'annual_mileage_of_user_before_joining_fyle'].astype('str')
        df_employees['perdiem_names'] = df_employees['perdiem_names'].astype('str')
        df_employees['joining_date'] = pd.to_datetime(df_employees['joining_date']).dt.strftime('%Y-%m-%d')
        df_expenses = pd.DataFrame(expenses)
        df_expenses['approved_by'] = df_expenses['approved_by'].map(lambda expense: expense[0] if expense else None)
        df_expenses['index_no'] = np.arange(len(df_expenses))
        df_expenses['approved_by'] = df_expenses['approved_by'].astype('str')
        df_expenses['export_ids'] = df_expenses['export_ids'].astype('str')
        df_expenses['custom_properties'] = df_expenses['custom_properties'].astype('str')
        df_expenses['locations'] = df_expenses['locations'].astype('str')
        df_reimbursements['export_ids'] = df_reimbursements['export_ids'].astype('str')
        df_employees.to_sql('employees', conn, if_exists='replace', index=False)
        df_settlements.to_sql('settlements', conn, if_exists='replace', index=False)
        df_reimbursements.to_sql('reimbursements', conn, if_exists='replace', index=False)
        df_expenses.to_sql('expenses', conn, if_exists='replace', index=False)
        return True
    return False
