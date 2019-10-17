drop table if exists invoices;
drop table if exists invoice_line_items;

CREATE TABLE invoices (
  InvoiceNumber TEXT PRIMARY KEY,
  Type TEXT,
  ContactID TEXT,
  Date TEXT,
  DueDate TEXT,
  LineAmountTypes TEXT,
  Status TEXT,
  Description TEXT,
  FOREIGN KEY (ContactID) REFERENCES employee_contact(ContactID)
);

CREATE TABLE invoice_line_items (
  InvoiceNumber TEXT,
  Description TEXT,
  Quantity INT,
  UnitAmount INT,
  AccountCode INT,
  FOREIGN KEY (AccountCode) REFERENCES  category_account(AccountCode),
  FOREIGN KEY (InvoiceNumber) REFERENCES invoices(InvoiceNumber)
);

-- SQL query to transform settlements into invoices

insert into invoices -- (InvoiceNumber, Type, ContactID, Date, DueDate, LineAmountTypes, Status, Description)
select s.id as InvoiceNumber,
  'ACCPAY' as Type, -- Using ACCPAY for bills
  e.ContactID as ContactID,
  s.opening_date as Date,
  s.closing_date as DueDate,
  'Exclusive' as LineAmountTypes, -- Using exclusive by default
  'SUBMITTED' as Status,   -- Using SUBMITTED adds to awaiting approval section, else by default adds to draft
  (s.employee_email || '-' || s.org_name || '-' || s.id) as Description
from
  settlements s
  LEFT JOIN employee_contact e on e.EmployeeEmail = s.employee_email;


-- SQL query to transform expenses into invoice_line_items

insert into invoice_line_items -- (InvoiceNumber, Description, Quantity, UnitAmount, AccountCode )
select i.InvoiceNumber as InvoiceNumber,
  (e.purpose || ' (' || e.expense_number || '-' || e.id || ')') as Description,
  1 as Quantity, -- Using 1 as default line item quantity
  e.amount as UnitAmount,
  c.AccountCode as AccountCode
from
  expenses e
  LEFT JOIN invoices i on i.InvoiceNumber = e.settlement_id
  LEFT JOIN category_account c on c.CategoryName = e.category_name
