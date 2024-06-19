INSERT INTO bank(`BankID`, `BankName`, `Address`, `ImagePath`)VALUES
(3, '中国工商银行', '北京市东城区东单大街1号', 'upload/3_ICBC.png'),
(4, '中国农业银行', '北京市西城区西单大街1号', 'upload/4_ABC.png');

INSERT INTO department(`DepartmentID`, `DepartmentName`, `BankID`)VALUES
(1, '个人业务部', 3),
(2, '公司业务部', 3),
(3, '个人业务部', 4),
(4, '公司业务部', 4);

INSERT INTO employee(`EmployeeID`, `EmployeeName`, `Position`, `DepartmentID`, `BankID`)VALUES
(1, '张三', '业务员', 1, 3),
(2, '李四', '业务员', 1, 3),
(3, '王五', '业务员', 2, 3),
(4, '赵六', '业务员', 2, 3),
(5, '钱七', '业务员', 3, 4),
(6, '孙八', '业务员', 3, 4),
(7, '周九', '业务员', 4, 4),
(8, '吴十', '业务员', 4, 4);

INSERT INTO customer(`CustomerID`, `CustomerName`, `Address`, `ContactInfo`, `VipStatus`, `BankID`)VALUES
(1, '张三', '北京市海淀区', '123456789', 'VIP', 3),
(2, '李四', '北京市朝阳区', '123456789', 'VIP', 3),
(3, '王五', '北京市东城区', '123456789', 'VIP', 3),
(4, '赵六', '北京市西城区', '123456789', 'VIP', 3),
(5, '钱七', '北京市海淀区', '123456789', 'VIP', 4),
(6, '孙八', '北京市朝阳区', '123456789', 'VIP', 4),
(7, '周九', '北京市东城区', '123456789', 'VIP', 4),
(8, '吴十', '北京市西城区', '123456789', 'VIP', 4);

INSERT INTO account(`AccountID`, 