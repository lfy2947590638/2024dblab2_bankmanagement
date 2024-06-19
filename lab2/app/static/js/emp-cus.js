/* static/js/emp-cus.js */

function fetchEmployeeCustomers() {
  fetch("/api/emp-cus")
      .then((response) => response.json())
      .then((data) => {
          console.log("Fetched employee-customer relations:", data); // 调试信息
          let tableBody = document.getElementById("employeeCustomerTableBody");
          tableBody.innerHTML = ""; // 清空现有的表格内容
          data.forEach((relation) => {
              let row = tableBody.insertRow();
              row.insertCell(0).innerText = relation.EmployeeID;
              row.insertCell(1).innerText = relation.CustomerID;
              let actionsCell = row.insertCell(2);
              actionsCell.innerHTML = `
                  <button onclick="editEmployeeCustomer(${relation.EmployeeID}, ${relation.CustomerID})">Edit</button>
                  <button onclick="deleteEmployeeCustomer(${relation.EmployeeID}, ${relation.CustomerID})">Delete</button>
              `;
          });
      })
      .catch((error) => {
          console.error("Error fetching employee-customer relations:", error);
      });
}

function addEmployeeCustomer(event) {
  event.preventDefault();
  let employeeID = document.getElementById("addEmployeeCustomerEmployeeID").value;
  let customerID = document.getElementById("addEmployeeCustomerCustomerID").value;

  fetch("/api/emp-cus", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({
          EmployeeID: employeeID,
          CustomerID: customerID,
      }),
  })
      .then((response) => response.json())
      .then((data) => {
          console.log("Employee-Customer relation added:", data);
          fetchEmployeeCustomers();
          document.getElementById("addEmployeeCustomerForm").reset();
      })
      .catch((error) => {
          console.error("Error adding Employee-Customer relation:", error);
      });
}

function editEmployeeCustomer(employeeID, customerID) {
  document.getElementById("editEmployeeCustomerEmployeeID").value = employeeID;
  document.getElementById("editEmployeeCustomerCustomerID").value = customerID;
}

function updateEmployeeCustomer(event) {
  event.preventDefault();
  let employeeID = document.getElementById("editEmployeeCustomerEmployeeID").value;
  let customerID = document.getElementById("editEmployeeCustomerCustomerID").value;
  let newEmployeeID = document.getElementById("editEmployeeCustomerNewEmployeeID").value;
  let newCustomerID = document.getElementById("editEmployeeCustomerNewCustomerID").value;

  fetch(`/api/emp-cus/${employeeID}/${customerID}`, {
      method: "PUT",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({
          EmployeeID: newEmployeeID,
          CustomerID: newCustomerID,
      }),
  })
      .then((response) => response.json())
      .then((data) => {
          console.log("Employee-Customer relation updated:", data);
          fetchEmployeeCustomers();
          document.getElementById("editEmployeeCustomerForm").reset();
      })
      .catch((error) => {
          console.error("Error updating Employee-Customer relation:", error);
      });
}

function deleteEmployeeCustomer(employeeID, customerID) {
  fetch(`/api/emp-cus/${employeeID}/${customerID}`, {
      method: "DELETE",
  })
      .then((response) => response.json())
      .then((data) => {
          console.log("Employee-Customer relation deleted:", data);
          fetchEmployeeCustomers();
      })
      .catch((error) => {
          console.error("Error deleting Employee-Customer relation:", error);
      });
}

document.addEventListener("DOMContentLoaded", function () {
  fetchEmployeeCustomers();
});
