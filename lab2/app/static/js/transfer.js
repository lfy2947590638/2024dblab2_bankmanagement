// static/js/transfer.js

function transferFunds(event) {
    event.preventDefault();
    let fromAccountID = document.getElementById('fromAccountID').value;
    let toAccountID = document.getElementById('toAccountID').value;
    let amount = document.getElementById('amount').value;

    fetch('/api/transfer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            fromAccountID: fromAccountID,
            toAccountID: toAccountID,
            amount: amount
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Transfer result:', data);
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            alert('Transfer completed successfully');
            document.getElementById('transferForm').reset();
        }
    })
    .catch(error => console.error('Error transferring funds:', error));
}
