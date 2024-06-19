class Bank:
    def __init__(self, BankID, BankName, Address):
        self.BankID = BankID
        self.BankName = BankName
        self.Address = Address

class Customer:
    def __init__(self, CustomerID, CustomerName, Address, ContactInfo):
        self.CustomerID = CustomerID
        self.CustomerName = CustomerName
        self.Address = Address
        self.ContactInfo = ContactInfo

class Account:
    def __init__(self, AccountID, AccountType, Balance, OpenDate, CustomerID):
        self.AccountID = AccountID
        self.AccountType = AccountType
        self.Balance = Balance
        self.OpenDate = OpenDate
        self.CustomerID = CustomerID

class Loan:
    def __init__(self, LoanID, LoanAmount, LoanType, LoanDate, CustomerID):
        self.LoanID = LoanID
        self.LoanAmount = LoanAmount
        self.LoanType = LoanType
        self.LoanDate = LoanDate
        self.CustomerID = CustomerID

class Department:
    def __init__(self, DepartmentID, DepartmentName, BankID):
        self.DepartmentID = DepartmentID
        self.DepartmentName = DepartmentName
        self.BankID = BankID

class Employee:
    def __init__(self, EmployeeID, EmployeeName, Position, DepartmentID, BankID):
        self.EmployeeID = EmployeeID
        self.EmployeeName = EmployeeName
        self.Position = Position
        self.DepartmentID = DepartmentID
        self.BankID = BankID

class EmployeeCustomer:
    def __init__(self, EmployeeID, CustomerID):
        self.EmployeeID = EmployeeID
        self.CustomerID = CustomerID