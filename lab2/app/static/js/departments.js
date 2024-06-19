/* static/js/departments.js */

function fetchDepartments() {
  fetch("/api/departments")
    .then((response) => response.json())
    .then((data) => {
      console.log("Fetched departments:", data); // 调试信息
      let tableBody = document.getElementById("departmentTableBody");
      tableBody.innerHTML = ""; // 清空现有的表格内容
      data.forEach((department) => {
        let row = tableBody.insertRow();
        row.insertCell(0).innerText = department.DepartmentID;
        row.insertCell(1).innerText = department.DepartmentName;
        let actionsCell = row.insertCell(2);
        actionsCell.innerHTML = `
                    <button onclick="editDepartment(${department.DepartmentID}, '${department.DepartmentName}')">Edit</button>
                    <button onclick="deleteDepartment(${department.DepartmentID})">Delete</button>`;
      });
    })
    .catch((error) => {
      console.error("Error fetching departments:", error);
    });
}

function addDepartment(event) {
  event.preventDefault();
  let departmentID = document.getElementById("addDepartmentID").value;
  let departmentName = document.getElementById("addDepartmentName").value;

  fetch("/api/departments", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      DepartmentID: departmentID,
      DepartmentName: departmentName,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Department added:", data);
      fetchDepartments();
      document.getElementById("addDepartmentForm").reset();
    })
    .catch((error) => {
      console.error("Error adding department:", error);
    });
}

function editDepartment(id, name) {
  document.getElementById("editDepartmentID").value = id;
  document.getElementById("editDepartmentName").value = name;
}

function updateDepartment(event) {
  event.preventDefault();
  let departmentID = document.getElementById("editDepartmentID").value;
  let departmentName = document.getElementById("editDepartmentName").value;

  fetch(`/api/departments/${departmentID}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      DepartmentID: departmentID,
      DepartmentName: departmentName,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Department updated:", data);
      fetchDepartments();
      document.getElementById("editDepartmentForm").reset();
    })
    .catch((error) => {
      console.error("Error updating department:", error);
    });
}

function deleteDepartment(id) {
  fetch(`/api/departments/${id}`, {
    method: "DELETE",
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Department deleted:", data);
      fetchDepartments();
    })
    .catch((error) => {
      console.error("Error deleting department:", error);
    });
}

document.addEventListener("DOMContentLoaded", function () {
  fetchDepartments();
});
