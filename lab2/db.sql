-- 创建数据库
DROP DATABASE IF EXISTS BankManagementSystem;
CREATE DATABASE BankManagementSystem;
USE BankManagementSystem;

-- 创建银行表
CREATE TABLE Bank (
    BankID INT PRIMARY KEY AUTO_INCREMENT,
    BankName VARCHAR(100) NOT NULL,
    Address VARCHAR(255),
    ImagePath VARCHAR(255)
);

-- 创建客户表
CREATE TABLE Customer (
    CustomerID INT,
    CustomerName VARCHAR(100) NOT NULL,
    Address VARCHAR(255),
    ContactInfo VARCHAR(50),
    VipStatus VARCHAR(50),
    BankID INT,
    PRIMARY KEY (CustomerID, BankID),
    FOREIGN KEY (BankID) REFERENCES Bank(BankID) ON DELETE CASCADE
);

-- 创建账户表
CREATE TABLE Account (
    AccountID INT,
    AccountType VARCHAR(50),
    Balance DECIMAL(10, 2),
    OpenDate DATE,
    CustomerID INT,
    BankID INT,
    PRIMARY KEY (AccountID, BankID),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE,
    Foreign Key (BankID) REFERENCES Bank(BankID) ON DELETE CASCADE
);

-- 创建贷款表
CREATE TABLE Loan (
    LoanID INT,
    LoanAmount DECIMAL(10, 2),
    LoanType VARCHAR(50),
    InterestRate DECIMAL(5, 2) NOT NULL DEFAULT 0.00,
    LoanDate DATE,
    CustomerID INT,
    BankID INT,
    PRIMARY KEY (LoanID, BankID),
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE,
    FOREIGN KEY (BankID) REFERENCES Bank(BankID) ON DELETE CASCADE
);

-- 创建部门表
CREATE TABLE Department (
    DepartmentID INT,
    DepartmentName VARCHAR(100),
    BankID INT,
    PRIMARY KEY (DepartmentID, BankID),
    FOREIGN KEY (BankID) REFERENCES Bank(BankID) ON DELETE CASCADE
);

-- 创建员工表
CREATE TABLE Employee (
    EmployeeID INT,
    EmployeeName VARCHAR(100) NOT NULL,
    Position VARCHAR(50),
    DepartmentID INT,
    BankID INT,
    PRIMARY KEY (EmployeeID, BankID),
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID) ON DELETE CASCADE,
    FOREIGN KEY (BankID) REFERENCES Bank(BankID) ON DELETE CASCADE
);

-- 创建员工负责客户的中间表
CREATE TABLE EmployeeCustomer (
    EmployeeID INT,
    CustomerID INT,
    bankID INT,
    PRIMARY KEY (EmployeeID, CustomerID, bankID),
    FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID) on delete cascade,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) on delete cascade,
    FOREIGN KEY (BankID) REFERENCES Bank(BankID) on delete cascade
);


-- 插入示例数据
INSERT INTO Bank (`BankID`, `BankName`, `Address`, `ImagePath`) VALUES
(1, '中国建设银行', '北京市海淀区', 'upload/1_CCB.png'),
(2, '交通银行', '北京市朝阳区', 'upload/2_BOCOM.png');

INSERT INTO Customer (`CustomerID`, `CustomerName`, `Address`, `ContactInfo`, `VipStatus`, `BankID`) VALUES
(1, 'Alice Johnson', '123 Main St', '123-456-7890', 'Regular', 1),
(2, 'Bob Williams', '456 Elm St', '456-789-0123', 'Regular', 1),
(3, 'Charlie Brown', '789 Oak St', '789-012-3456', 'Regular', 1),
(4, 'David Davis', '234 Pine St', '234-567-8901', 'Regular', 1),
(1, 'Lily Johnson', '123 Main St', '123-456-7890', 'Regular', 2),
(2, 'Lucy Williams', '456 Elm St', '456-789-0123', 'Regular', 2),
(3, 'Mike Brown', '789 Oak St', '789-012-3456', 'Regular', 2),
(4, 'Nancy Davis', '234 Pine St', '234-567-8901', 'Regular', 2);

INSERT INTO Department (DepartmentID, DepartmentName, BankID) VALUES
(1, 'HR', 1),
(2, 'Finance', 1),
(3, 'IT', 1),
(4, 'HR', 2),
(5, 'Finance', 2),
(6, 'IT', 2);

INSERT INTO Employee (`EmployeeID`, `EmployeeName`, `Position`, `DepartmentID`, `BankID`) VALUES
(1, 'Alice Johnson', 'Manager', 1, 1),
(2, 'Bob Williams', 'IT Specialist', 3, 1),
(3, 'Charlie Brown', 'Clerk', 2, 1),
(4, 'David Davis', 'Clerk', 2, 1),
(1, 'Lily Johnson', 'Manager', 4, 2),
(2, 'Lucy Williams', 'IT Specialist', 6, 2),
(3, 'Mike Brown', 'Clerk', 5, 2),
(4, 'Nancy Davis', 'Clerk', 5, 2);

INSERT INTO Account (`AccountID`, `AccountType`, `Balance`, `OpenDate`, `CustomerID`, `BankID`) VALUES
(1, 'Checking', 1000.00, '2022-01-01', 1, 1),
(2, 'Savings', 2000.00, '2022-02-01', 2, 1),
(3, 'Checking', 3000.00, '2022-03-01', 3, 1),
(4, 'Savings', 4000.00, '2022-04-01', 4, 1),
(1, 'Checking', 5000.00, '2022-01-01', 1, 2),
(2, 'Savings', 6000.00, '2022-02-01', 2, 2),
(3, 'Checking', 7000.00, '2022-03-01', 3, 2),
(4, 'Savings', 8000.00, '2022-04-01', 4, 2);

INSERT INTO Loan (`LoanID`, `LoanAmount`, `LoanType`, `InterestRate`, `LoanDate`, `CustomerID`, `BankID`) VALUES
(1, 10000.00, 'Personal', 0.03, '2022-01-01', 1, 1),
(2, 20000.00, 'Mortgage', 0.04, '2022-02-01', 2, 1),
(3, 30000.00, 'Personal', 0.02, '2022-03-01', 3, 1),
(4, 40000.00, 'Mortgage', 0.06, '2022-04-01', 4, 1),
(1, 50000.00, 'Personal', 0.01, '2022-01-01', 1, 2),
(2, 60000.00, 'Mortgage', 0.04, '2022-02-01', 2, 2),
(3, 70000.00, 'Personal', 0.02, '2022-03-01', 3, 2),
(4, 80000.00, 'Mortgage', 0.05, '2022-04-01', 4, 2);

INSERT INTO EmployeeCustomer (EmployeeID, CustomerID, BankID) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 3, 1),
(4, 4, 1),
(1, 1, 2),
(2, 2, 2),
(3, 3, 2),
(4, 4, 2);