function fetchEmployees() {
    fetch('/api/employees')
        .then(response => response.json())
        .then(data => {
            let tableBody = document.querySelector('#employeesTable tbody');
            tableBody.innerHTML = '';
            data.forEach(employee => {
                let row = tableBody.insertRow();
                row.insertCell(0).innerText = employee.EmployeeID;
                row.insertCell(1).innerText = employee.EmployeeName;
                row.insertCell(2).innerText = employee.Position;
                row.insertCell(3).innerText = employee.DepartmentID;
                let actionsCell = row.insertCell(4);
                actionsCell.innerHTML = `
                    <button onclick="editEmployee(${employee.EmployeeID}, '${employee.EmployeeName}', '${employee.Position}', ${employee.DepartmentID})">Edit</button>
                    <button onclick="deleteEmployee(${employee.EmployeeID})">Delete</button>
                `;
            });
        })
        .catch(error => console.error('Error fetching employees:', error));
}

function addEmployee(event) {
    event.preventDefault();
    let employeeID = document.getElementById('addEmployeeID').value;
    let employeeName = document.getElementById('addEmployeeName').value;
    let position = document.getElementById('addPosition').value;
    let departmentID = document.getElementById('addDepartmentID').value;

    fetch('/api/employees', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            EmployeeID: employeeID,
            EmployeeName: employeeName,
            Position: position,
            DepartmentID: departmentID
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Employee added:', data);
        fetchEmployees();
        document.getElementById('addEmployeeForm').reset();
    })
    .catch(error => console.error('Error adding employee:', error));
}

function editEmployee(employeeID, employeeName, position, departmentID) {
    document.getElementById('editEmployeeID').value = employeeID;
    document.getElementById('editEmployeeName').value = employeeName;
    document.getElementById('editPosition').value = position;
    document.getElementById('editDepartmentID').value = departmentID;
}

function updateEmployee(event) {
    event.preventDefault();
    let employeeID = document.getElementById('editEmployeeID').value;
    let employeeName = document.getElementById('editEmployeeName').value;
    let position = document.getElementById('editPosition').value;
    let departmentID = document.getElementById('editDepartmentID').value;

    fetch(`/api/employees/${employeeID}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            EmployeeName: employeeName,
            Position: position,
            DepartmentID: departmentID
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Employee updated:', data);
        fetchEmployees();
        document.getElementById('editEmployeeForm').reset();
    })
    .catch(error => console.error('Error updating employee:', error));
}

function deleteEmployee(employeeID) {
    fetch(`/api/employees/${employeeID}`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        console.log('Employee deleted:', data);
        fetchEmployees();
    })
    .catch(error => console.error('Error deleting employee:', error));
}

document.addEventListener('DOMContentLoaded', fetchEmployees);
