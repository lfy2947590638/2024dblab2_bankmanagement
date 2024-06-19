from app import app, mysql
from flask import render_template, request, redirect, url_for, session, jsonify, flash, Flask
from img import UploadForm, allowed_file
from werkzeug.utils import secure_filename
import os

@app.route('/')
def index():
    if 'selected_bank' not in session:
        return redirect(url_for('select_bank'))
    
    selected_bank = None
    total_deposits = 0.00
    total_loans = 0.00
    image = None

    if 'selected_bank' in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Bank WHERE BankID = %s", (session['selected_bank'],))
        selected_bank = cur.fetchone()
        # 获取总存款额
        cur.execute("SELECT GetTotalDeposits(%s)", (session['selected_bank'],))
        total_deposits = list(cur.fetchone().values())[0]     
        # 获取总贷款额
        cur.execute("SELECT GetTotalLoans(%s)", (session['selected_bank'],))
        total_loans = list(cur.fetchone().values())[0]
        # 获取背景图片路径
        image = selected_bank['ImagePath']
        print(image)
        cur.close()
        # print(selected_bank) # 调试输出
        # session.clear() # 清空session
    return render_template('index.html', selected_bank=selected_bank, total_deposits=total_deposits, total_loans=total_loans, image=image)


@app.route('/select_bank', methods=['GET', 'POST'])
def select_bank():
    if request.method == 'POST':
        session['selected_bank'] = request.form['bankID']
        return redirect(url_for('index'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Bank")
    rows = cur.fetchall()
    cur.close()
    return render_template('select_bank.html', banks=rows)

# 测试数据库连接
@app.route('/test_db_connection')
def test_db_connection():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        cur.close()
        return jsonify({'result': result})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# 获取所有客户
@app.route('/customers', methods=['GET'])
def customers():
    return render_template('customers.html')

@app.route('/api/customers', methods=['GET'])
def get_customers():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Customer where bankID = %s", (session['selected_bank'],))
        rows = cur.fetchall()
        cur.close()
        print(rows) # 调试输出
        return jsonify(rows)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# 添加客户
@app.route('/api/customers', methods=['POST'])
def add_customer():
    data = request.get_json()
    print(data)
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Customer (CustomerID, CustomerName, Address, ContactInfo, VipStatus, BankID) VALUES (%s, %s, %s, %s, %s, %s)",
                (data['CustomerID'], data['CustomerName'], data['Address'], data['ContactInfo'], data['VipStatus'], session['selected_bank']))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Customer added successfully'})

# 更新客户信息
@app.route('/api/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE Customer SET CustomerID=%s, CustomerName=%s, Address=%s, ContactInfo=%s, VipStatus=%s WHERE CustomerID=%s AND BankID=%s",
                (data['CustomerID'], data['CustomerName'], data['Address'], data['ContactInfo'], data['VipStatus'], id, session['selected_bank']))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Customer updated successfully'})

# 删除客户
@app.route('/api/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Customer WHERE CustomerID=%s AND BankID=%s", (id, session['selected_bank']))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Customer deleted successfully'})

# 获取所有员工-客户关系
@app.route('/emp-cus', methods=['GET'])
def employee_customers():
    return render_template('emp-cus.html')

@app.route('/api/emp-cus', methods=['GET'])
def get_employee_customers():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM EmployeeCustomer where bankID = %s", (session['selected_bank'],))
        rows = cur.fetchall()
        cur.close()
        return jsonify(rows)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/emp-cus', methods=['POST'])
def add_employee_customer():
    data = request.get_json()
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO EmployeeCustomer (EmployeeID, CustomerID, BankID) VALUES (%s, %s, %s)",
                    (data['EmployeeID'], data['CustomerID'], session['selected_bank']))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Employee-Customer relation added successfully'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/emp-cus/<int:employee_id>/<int:customer_id>', methods=['PUT'])
def update_employee_customer(employee_id, customer_id):
    data = request.get_json()
    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE EmployeeCustomer SET EmployeeID=%s, CustomerID=%s WHERE EmployeeID=%s AND CustomerID=%s AND BankID=%s",
                    (data['EmployeeID'], data['CustomerID'], employee_id, customer_id, session['selected_bank']))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Employee-Customer relation updated successfully'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/emp-cus/<int:employee_id>/<int:customer_id>', methods=['DELETE'])
def delete_employee_customer(employee_id, customer_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM EmployeeCustomer WHERE EmployeeID=%s AND CustomerID=%s AND BankID=%s",
                    (employee_id, customer_id, session['selected_bank']))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Employee-Customer relation deleted successfully'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# 获取所有部门
@app.route('/departments', methods=['GET'])
def departments():
    return render_template('departments.html')

@app.route('/api/departments', methods=['GET'])
def get_departments():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Department where bankID = %s", (session['selected_bank'],))
        rows = cur.fetchall()
        cur.close()
        return jsonify(rows)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/departments', methods=['POST'])
def add_department():
    data = request.get_json()
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Department (DepartmentID, DepartmentName, BankID) VALUES (%s, %s, %s)",
                    (data['DepartmentID'], data['DepartmentName'], session['selected_bank']))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Department added successfully'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/departments/<int:id>', methods=['PUT'])
def update_department(id):
    data = request.get_json()
    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Department SET DepartmentID=%s, DepartmentName=%s WHERE DepartmentID=%s AND BankID=%s",
                    (data['DepartmentID'], data['DepartmentName'], id, session['selected_bank']))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Department updated successfully'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/departments/<int:id>', methods=['DELETE'])
def delete_department(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Department WHERE DepartmentID=%s AND BankID=%s", (id, session['selected_bank']))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Department deleted successfully'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/accounts', methods=['GET'])
def accounts():
    return render_template('accounts.html')

@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Account WHERE BankID = %s", (session['selected_bank'],))
        accounts = cur.fetchall()
        # print(accounts) # 调试输出
        cur.close()
        return jsonify(accounts)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts', methods=['POST'])
def add_account():
    try:
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Account (AccountID, AccountType, Balance, OpenDate, CustomerID, BankID) VALUES (%s, %s, %s, %s, %s, %s)",
                    (data['AccountID'], data['AccountType'], data['Balance'], data['OpenDate'], data['CustomerID'], session['selected_bank']))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Account added successfully'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/<int:account_id>', methods=['PUT'])
def update_account(account_id):
    try:
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Account SET AccountType=%s, Balance=%s, OpenDate=%s WHERE AccountID=%s AND BankID=%s",
                    (data['AccountType'], data['Balance'], data['OpenDate'],  account_id, session['selected_bank']))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Account updated successfully'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/accounts/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Account WHERE AccountID=%s AND BankID=%s", (account_id, session['selected_bank']))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Account deleted successfully'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

# 新增API端点来调用存储过程
@app.route('/api/add_bonus_to_savings', methods=['POST'])
def add_bonus_to_savings():
    if 'selected_bank' not in session:
        return jsonify({"error": "No bank selected"}), 400
    
    bank_id = session['selected_bank']
    bonus_amount = 100.00  # 固定的奖金金额
    cur = mysql.connection.cursor()
    cur.execute("CALL AddBonusToSavings(%s, %s)", (bank_id, bonus_amount))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Bonus added to savings successfully'})

@app.route('/transfer', methods=['GET'])
def transfer():
    return render_template('transfer.html')

@app.route('/api/transfer', methods=['POST'])
def transfer_funds():
    data = request.get_json()
    from_account = data['fromAccountID']
    to_account = data['toAccountID']
    amount = data['amount']
    bank_id = session.get('selected_bank')
    state = -1

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("CALL TransferFunds(%s, %s, %s, %s, @state)", (from_account, to_account, amount, bank_id))
        cursor.execute("SELECT @state")
        state = cursor.fetchone()['@state']
        cursor.close()
        
        if state == 0:
            return jsonify({'message': 'Transfer completed successfully'})
        elif state == 2:
            return jsonify({'error': 'One or both accounts do not exist or do not belong to the same bank'}), 400
        elif state == 3:
            return jsonify({'error': 'Insufficient funds'}), 400
        else:
            return jsonify({'error': 'Transfer failed'}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

    
@app.route('/loans', methods=['GET'])
def loans():
    return render_template('loans.html')

@app.route('/api/loans', methods=['GET'])
def get_loans():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Loan WHERE BankID = %s", (session['selected_bank'],))
        loans = cur.fetchall()
        cur.close()
        return jsonify(loans)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/loans', methods=['POST'])
def add_loan():
    try:
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Loan (LoanID, LoanType, LoanAmount, LoanDate, InterestRate, CustomerID, BankID) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (data['LoanID'], data['LoanType'], data['LoanAmount'], data['LoanDate'], data['InterestRate'], data['CustomerID'], session['selected_bank']))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Loan added successfully'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/loans/<int:loan_id>', methods=['PUT'])
def update_loan(loan_id):
    try:
        data = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Loan SET LoanAmount=%s, LoanType=%s, LoanDate=%s, InterestRate=%s WHERE LoanID=%s AND BankID=%s",
                    (data['LoanAmount'], data['LoanType'], data['LoanDate'], data['InterestRate'], loan_id, session['selected_bank']))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Loan updated successfully'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/loans/<int:loan_id>', methods=['DELETE'])
def delete_loan(loan_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Loan WHERE LoanID=%s AND BankID=%s", (loan_id, session['selected_bank']))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Loan deleted successfully'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/employees', methods=['GET'])
def employees():
    return render_template('employees.html')

@app.route('/api/employees', methods=['GET'])
def get_employees():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Employee WHERE BankID = %s", (session['selected_bank'],))
        employees = cur.fetchall()
        cur.close()
        return jsonify(employees)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/employees', methods=['POST'])
def add_employee():
    try:
        data = request.get_json()
        print(data)
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Employee (EmployeeID, EmployeeName, Position, DepartmentID, BankID) VALUES (%s, %s, %s, %s, %s)",
                    (data['EmployeeID'], data['EmployeeName'], data['Position'], data['DepartmentID'], session['selected_bank']))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Employee added successfully'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    try:
        data = request.get_json()
        print(data)
        cur = mysql.connection.cursor()
        cur.execute("UPDATE Employee SET EmployeeName=%s, Position=%s, DepartmentID=%s WHERE EmployeeID=%s AND BankID=%s",
                    (data['EmployeeName'], data['Position'], data['DepartmentID'], employee_id, session['selected_bank']))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Employee updated successfully'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM Employee WHERE EmployeeID=%s AND BankID=%s", (employee_id, session['selected_bank']))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Employee deleted successfully'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/upload_bank_image', methods=['GET', 'POST'])
def upload_bank_image():
    form = UploadForm()
    if form.validate_on_submit():   # 如果表单数据被提交且通过了验证
        f = form.file.data
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            # bank_id = form.user_id.data
            bank_id = session['selected_bank']
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{bank_id}_{filename}")
            # 确保上传文件夹存在
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            # 保存文件到指定路径
            f.save(upload_path)
            print(f"File saved to {upload_path}")
            # 保存图片路径到数据库
            cur = mysql.connection.cursor()
            cur.execute("UPDATE Bank SET ImagePath = %s WHERE BankID = %s", ('/upload/' + f"{bank_id}_{filename}", bank_id))
            mysql.connection.commit()
            cur.close()
            flash('上传成功')
            return redirect(url_for('index'))  # 上传成功后重定向到主页
        else:
            print('文件类型不被允许')
    else:
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Error in {getattr(form, field).label.text}: {error}")

    return render_template('upload_bank_image.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
