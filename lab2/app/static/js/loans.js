function fetchLoans() {
    fetch('/api/loans')
        .then(response => response.json())
        .then(data => {
            let tableBody = document.querySelector('#loansTable tbody');
            tableBody.innerHTML = '';
            data.forEach(loan => {
                let row = tableBody.insertRow();
                row.insertCell(0).innerText = loan.LoanID;
                row.insertCell(1).innerText = loan.LoanAmount;
                row.insertCell(2).innerText = loan.LoanType;
                row.insertCell(3).innerText = loan.LoanDate;
                row.insertCell(4).innerText = loan.InterestRate;
                row.insertCell(5).innerText = loan.CustomerID;
                let actionsCell = row.insertCell(6);
                actionsCell.innerHTML = `
                    <button onclick="editLoan(${loan.LoanID}, ${loan.LoanAmount}, '${loan.LoanType}', '${loan.LoanDate}', ${loan.InterestRate}, ${loan.CustomerID})">Edit</button>
                    <button onclick="deleteLoan(${loan.LoanID})">Delete</button>
                `;
            });
        })
        .catch(error => console.error('Error fetching loans:', error));
}

function addLoan(event) {
    event.preventDefault();
    let loanID = document.getElementById('addLoanID').value;
    let loanAmount = document.getElementById('addLoanAmount').value;
    let loanType = document.getElementById('addLoanType').value;
    let loanDate = document.getElementById('addLoanDate').value;
    let interestRate = document.getElementById('addInterestRate').value;
    let customerID = document.getElementById('addCustomerID').value;

    if (!loanDate) {
        loanDate = new Date().toISOString().split('T')[0]; // 设置为当前日期
    }

    fetch('/api/loans', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            LoanID: loanID,
            LoanAmount: loanAmount,
            LoanType: loanType,
            LoanDate: loanDate,
            InterestRate: interestRate,
            CustomerID: customerID
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Loan added:', data);
        fetchLoans();
        document.getElementById('addLoanForm').reset();
    })
    .catch(error => console.error('Error adding loan:', error));
}

function editLoan(loanID, loanAmount, loanType, loanDate, interestRate, customerID) {
    document.getElementById('editLoanID').value = loanID;
    document.getElementById('editLoanAmount').value = loanAmount;
    document.getElementById('editLoanType').value = loanType;
    document.getElementById('editLoanDate').value = loanDate;
    document.getElementById('editInterestRate').value = interestRate;
    document.getElementById('editCustomerID').value = customerID;
}

function updateLoan(event) {
    event.preventDefault();
    let loanID = document.getElementById('editLoanID').value;
    let loanAmount = document.getElementById('editLoanAmount').value;
    let loanType = document.getElementById('editLoanType').value;
    let loanDate = document.getElementById('editLoanDate').value;
    let interestRate = document.getElementById('editInterestRate').value;

    if (!loanDate) {
        loanDate = new Date().toISOString().split('T')[0]; // 设置为当前日期
    }

    fetch(`/api/loans/${loanID}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            LoanAmount: loanAmount,
            LoanType: loanType,
            LoanDate: loanDate,
            InterestRate: interestRate
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Loan updated:', data);
        fetchLoans();
        document.getElementById('editLoanForm').reset();
    })
    .catch(error => console.error('Error updating loan:', error));
}

function deleteLoan(loanID) {
    fetch(`/api/loans/${loanID}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        console.log('Loan deleted:', data);
        fetchLoans();
    })
    .catch(error => console.error('Error deleting loan:', error));
}

document.addEventListener('DOMContentLoaded', fetchLoans);
