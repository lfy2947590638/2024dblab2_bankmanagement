function fetchCustomers() {
  fetch("/api/customers")
    .then((response) => response.json())
    .then((data) => {
      console.log("Fetched customers:", data); // 调试信息
      let customerTable = document.getElementById("customerTableBody");
      customerTable.innerHTML = ""; // 清空现有的表格内容
      data.forEach((customer) => {
        let row = customerTable.insertRow();
        row.insertCell(0).innerText = customer.CustomerID;
        row.insertCell(1).innerText = customer.CustomerName;
        row.insertCell(2).innerText = customer.Address;
        row.insertCell(3).innerText = customer.ContactInfo;
        row.insertCell(4).innerText = customer.VipStatus;
        let actionsCell = row.insertCell(5);
        actionsCell.innerHTML = `
          <button onclick="editCustomer(${customer.CustomerID}, '${customer.CustomerName}', '${customer.Address}', '${customer.ContactInfo}', '${customer.VipStatus}')">Edit</button>
          <button onclick="deleteCustomer(${customer.CustomerID})">Delete</button>
        `;
      });
    })
    .catch((error) => {
      console.error("Error fetching customers:", error);
    });
}

function addCustomer(event) {
  event.preventDefault();
  let customerID = document.getElementById("addCustomerID").value;
  let customerName = document.getElementById("addCustomerName").value;
  let customerAddress = document.getElementById("addCustomerAddress").value;
  let customerContactInfo = document.getElementById("addCustomerContactInfo").value;
  let vipStatus = document.getElementById("addCustomerVipStatus").value;

  if (!vipStatus) {
    vipStatus = "Regular";
  }

  fetch("/api/customers", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      CustomerID: customerID,
      CustomerName: customerName,
      Address: customerAddress,
      ContactInfo: customerContactInfo,
      VipStatus: vipStatus,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Customer added:", data);
      fetchCustomers();
      document.getElementById("addCustomerForm").reset();
    })
    .catch((error) => {
      console.error("Error adding customer:", error);
    });
}

function editCustomer(id, name, address, contactInfo, vipStatus) {
  document.getElementById("editCustomerID").value = id;
  document.getElementById("editCustomerName").value = name;
  document.getElementById("editCustomerAddress").value = address;
  document.getElementById("editCustomerContactInfo").value = contactInfo;
  document.getElementById("editCustomerVipStatus").value = vipStatus;
}

function updateCustomer(event) {
  event.preventDefault();
  let customerID = document.getElementById("editCustomerID").value;
  let customerName = document.getElementById("editCustomerName").value;
  let customerAddress = document.getElementById("editCustomerAddress").value;
  let customerContactInfo = document.getElementById("editCustomerContactInfo").value;
  let vipStatus = document.getElementById("editCustomerVipStatus").value;

  if (!vipStatus) {
    vipStatus = "Regular";
  }

  fetch(`/api/customers/${customerID}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      CustomerID: customerID,
      CustomerName: customerName,
      Address: customerAddress,
      ContactInfo: customerContactInfo,
      VipStatus: vipStatus,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Customer updated:", data);
      fetchCustomers();
      document.getElementById("editCustomerForm").reset();
    })
    .catch((error) => {
      console.error("Error updating customer:", error);
    });
}

function deleteCustomer(id) {
  fetch(`/api/customers/${id}`, {
    method: "DELETE",
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Customer deleted:", data);
      fetchCustomers();
    })
    .catch((error) => {
      console.error("Error deleting customer:", error);
    });
}

document.addEventListener("DOMContentLoaded", function () {
  fetchCustomers();
});
