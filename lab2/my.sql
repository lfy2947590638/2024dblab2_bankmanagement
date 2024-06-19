DELIMITER //

DROP FUNCTION IF EXISTS GetTotalDeposits //

CREATE FUNCTION GetTotalDeposits(bank_id INT) 
RETURNS DECIMAL(10, 2)
DETERMINISTIC
BEGIN
    DECLARE total_deposits DECIMAL(10, 2);
    SELECT SUM(Balance) INTO total_deposits
    FROM Account
    WHERE BankID = bank_id;
    RETURN IFNULL(total_deposits, 0.00);
END //

DELIMITER;

DELIMITER //

DROP FUNCTION IF EXISTS GetTotalLoans //

CREATE FUNCTION GetTotalLoans(bank_id INT) 
RETURNS DECIMAL(10, 2)
DETERMINISTIC
BEGIN
    DECLARE total_loans DECIMAL(10, 2);
    SELECT SUM(LoanAmount) INTO total_loans
    FROM Loan
    WHERE BankID = bank_id;
    RETURN IFNULL(total_loans, 0.00);
END //

DELIMITER;

DELIMITER //

DROP PROCEDURE IF EXISTS AddBonusToSavings //

CREATE PROCEDURE AddBonusToSavings(bank_id INT, bonus_amount DECIMAL(10, 2))
BEGIN
    UPDATE Account
    SET Balance = Balance + bonus_amount
    WHERE AccountType = 'Savings' AND BankID = bank_id;
END //

DELIMITER;

DELIMITER //

DROP TRIGGER IF EXISTS AfterInsertAccount //

CREATE TRIGGER AfterInsertAccount
AFTER INSERT ON Account
FOR EACH ROW
BEGIN
    DECLARE total_savings DECIMAL(10, 2) DEFAULT 0.00;
    IF NEW.AccountType = 'Savings' THEN
        SELECT SUM(Balance) INTO total_savings
        FROM Account
        WHERE CustomerID = NEW.CustomerID AND AccountType = 'Savings' AND BankID = NEW.BankID;
        IF total_savings >= 10000 THEN
            UPDATE Customer
            SET VipStatus = 'VIP'
            WHERE CustomerID = NEW.CustomerID AND BankID = NEW.BankID;
        END IF;
    END IF;
END //

DELIMITER ;


DELIMITER //

DROP TRIGGER IF EXISTS AfterUpdateAccount //

CREATE TRIGGER AfterUpdateAccount
AFTER UPDATE ON Account
FOR EACH ROW
BEGIN
    DECLARE total_savings DECIMAL(10, 2);
    IF NEW.AccountType = 'Savings' THEN
        SELECT SUM(Balance) INTO total_savings
        FROM Account
        WHERE CustomerID = NEW.CustomerID AND AccountType = 'Savings' AND BankID = NEW.BankID;
        
        IF total_savings >= 10000 THEN
            UPDATE Customer
            SET VipStatus = 'VIP'
            WHERE CustomerID = NEW.CustomerID AND BankID = NEW.BankID;
        END IF;
    END IF;
END //

DELIMITER;

DELIMITER //
DROP PROCEDURE IF EXISTS TransferFunds //
CREATE PROCEDURE TransferFunds(
    IN id_from INT,
    IN id_to INT,
    IN amount DECIMAL(10, 2),
    IN bank_id INT,
    OUT state INT
)
BEGIN
    DECLARE s INT DEFAULT 0;
    DECLARE a DECIMAL(10, 2);

    -- 定义一个通用的SQL异常处理程序
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET s = 1;

    START TRANSACTION;

    -- 检查账户是否存在且属于同一个银行
    SELECT COUNT(*) FROM Account WHERE (AccountID = id_from OR AccountID = id_to) AND BankID = bank_id INTO a;
    IF a < 2 THEN
        SET s = 2; -- 至少有一个账户不存在或不属于同一个银行
        ROLLBACK;
    ELSE
        -- 检查转出账户的余额
        SELECT Balance FROM Account WHERE AccountID = id_from AND BankID = bank_id INTO a;
        IF a < amount THEN
            SET s = 3; -- 余额不足
            ROLLBACK;
        ELSE
            -- 执行转账操作
            UPDATE Account SET Balance = Balance - amount WHERE AccountID = id_from AND BankID = bank_id;
            UPDATE Account SET Balance = Balance + amount WHERE AccountID = id_to AND BankID = bank_id;

            IF s = 0 THEN
                SET state = 0;
                COMMIT;
            ELSE
                SET state = -1000;
                ROLLBACK;
            END IF;
        END IF;
    END IF;
END //

DELIMITER ;




-- CALL TransferFunds(4, 2, 55, 2, @state);
-- SELECT @state;