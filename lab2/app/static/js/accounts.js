function fetchAccounts() {
    fetch('/api/accounts')
        .then(response => response.json())
        .then(data => {
            let tableBody = document.querySelector('#accountsTable tbody');
            tableBody.innerHTML = '';
            data.forEach(account => {
                let row = tableBody.insertRow();
                row.insertCell(0).innerText = account.AccountID;
                row.insertCell(1).innerText = account.AccountType;
                row.insertCell(2).innerText = account.Balance;
                row.insertCell(3).innerText = account.OpenDate;
                row.insertCell(4).innerText = account.CustomerID;
                let actionsCell = row.insertCell(5);
                actionsCell.innerHTML = `
                    <button onclick="editAccount(${account.AccountID}, '${account.AccountType}', ${account.Balance}, '${account.OpenDate}', ${account.CustomerID})">Edit</button>
                    <button onclick="deleteAccount(${account.AccountID})">Delete</button>
                `;
            });
        })
        .catch(error => console.error('Error fetching accounts:', error));
}

function addAccount(event) {
    event.preventDefault();
    let accountID = document.getElementById('addAccountID').value;
    let accountType = document.getElementById('addAccountType').value;
    let balance = document.getElementById('addBalance').value;
    let openDate = document.getElementById('addOpenDate').value;
    let customerID = document.getElementById('addCustomerID').value;

    if (!openDate) {
        openDate = new Date().toISOString().split('T')[0]; // 设置为当前日期
    }

    fetch('/api/accounts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            AccountID: accountID,
            AccountType: accountType,
            Balance: balance,
            OpenDate: openDate,
            CustomerID: customerID
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Account added:', data);
        fetchAccounts();
        document.getElementById('addAccountForm').reset();
    })
    .catch(error => console.error('Error adding account:', error));
}

function editAccount(accountID, accountType, balance, openDate, customerID) {
    document.getElementById('editAccountID').value = accountID;
    document.getElementById('editAccountType').value = accountType;
    document.getElementById('editBalance').value = balance;
    document.getElementById('editOpenDate').value = openDate;
    document.getElementById('editCustomerID').value = customerID;
}

function updateAccount(event) {
    event.preventDefault();
    let accountID = document.getElementById('editAccountID').value;
    let accountType = document.getElementById('editAccountType').value;
    let balance = document.getElementById('editBalance').value;
    let openDate = document.getElementById('editOpenDate').value;

    if (!openDate) {
        openDate = new Date().toISOString().split('T')[0]; // 设置为当前日期
    }

    fetch(`/api/accounts/${accountID}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            AccountType: accountType,
            Balance: balance,
            OpenDate: openDate
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Account updated:', data);
        fetchAccounts();
        document.getElementById('editAccountForm').reset();
    })
    .catch(error => console.error('Error updating account:', error));
}

function deleteAccount(accountID) {
    fetch(`/api/accounts/${accountID}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        console.log('Account deleted:', data);
        fetchAccounts();
    })
    .catch(error => console.error('Error deleting account:', error));
}

// 新增函数
function addBonusToSavings() {
    fetch('/api/add_bonus_to_savings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log('Bonus added to savings accounts:', data);
        fetchAccounts(); // 更新账户信息
    })
    .catch(error => console.error('Error adding bonus to savings accounts:', error));
}

document.addEventListener('DOMContentLoaded', fetchAccounts);
