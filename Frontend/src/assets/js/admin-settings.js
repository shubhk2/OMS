// Frontend/src/assets/js/admin-settings.js
// Handles admin settings page functionality

const API_BASE = 'http://127.0.0.1:5000';

function getAuthHeaders() {
  const token = localStorage.getItem('accessToken');
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  };
}

function escapeHtml(text) {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return String(text).replace(/[&<>"']/g, function(m) { return map[m]; });
}

function showAlert(message, type = 'success') {
  const container = document.getElementById('alert-container');
  const alert = document.createElement('div');
  alert.className = `alert alert-${type}`;
  alert.textContent = message;
  container.appendChild(alert);
  
  setTimeout(() => {
    alert.remove();
  }, 5000);
}

function switchTab(tabName) {
  // Hide all tab contents
  document.querySelectorAll('.tab-content').forEach(content => {
    content.classList.remove('active');
  });
  
  // Deactivate all tabs
  document.querySelectorAll('.tab').forEach(tab => {
    tab.classList.remove('active');
  });
  
  // Show selected tab content
  const selectedContent = document.getElementById(tabName);
  if (selectedContent) {
    selectedContent.classList.add('active');
  }
  
  // Activate selected tab
  const selectedTab = document.querySelector(`.tab[onclick="switchTab('${tabName}')"]`);
  if (selectedTab) {
    selectedTab.classList.add('active');
  }
  
  // Load data for the selected tab
  if (tabName === 'company-settings') {
    loadCompanySettings();
  } else if (tabName === 'roles') {
    loadRoles();
  } else if (tabName === 'specializations') {
    loadSpecializations();
  } else if (tabName === 'leave-types') {
    loadLeaveTypes();
  } else if (tabName === 'employees') {
    loadEmployees();
  }
}

// Company Settings Functions
async function loadCompanySettings() {
  try {
    const response = await fetch(`${API_BASE}/admin/settings`, {
      headers: getAuthHeaders()
    });
    
    if (!response.ok) {
      throw new Error('Failed to load company settings');
    }
    
    const settings = await response.json();
    const container = document.getElementById('company-settings-list');
    
    container.innerHTML = settings.map(setting => `
      <div class="form-group">
        <label>${escapeHtml(setting.description || setting.key)}</label>
        <div style="display: flex; gap: 10px;">
          <input type="text" id="setting-${setting.id}" value="${escapeHtml(setting.value)}" style="flex: 1;">
          <button class="btn btn-primary" onclick="updateSetting(${setting.id})">Update</button>
        </div>
        <small style="color: #666;">Key: ${escapeHtml(setting.key)}</small>
      </div>
    `).join('');
  } catch (error) {
    showAlert(error.message, 'error');
  }
}

async function updateSetting(settingId) {
  const input = document.getElementById(`setting-${settingId}`);
  const value = input.value;
  
  try {
    const response = await fetch(`${API_BASE}/admin/settings/${settingId}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify({ value })
    });
    
    if (!response.ok) {
      throw new Error('Failed to update setting');
    }
    
    showAlert('Setting updated successfully');
  } catch (error) {
    showAlert(error.message, 'error');
  }
}

// Roles Functions
async function loadRoles() {
  try {
    const response = await fetch(`${API_BASE}/admin/roles`, {
      headers: getAuthHeaders()
    });
    
    if (!response.ok) {
      throw new Error('Failed to load roles');
    }
    
    const roles = await response.json();
    const container = document.getElementById('roles-list');
    
    container.innerHTML = roles.map(role => `
      <li class="list-group-item">
        <span>${escapeHtml(role.name)} (ID: ${role.id})</span>
        <div>
          <button class="btn btn-danger" onclick="deleteRole(${role.id})">Delete</button>
        </div>
      </li>
    `).join('');
  } catch (error) {
    showAlert(error.message, 'error');
  }
}

async function addRole() {
  const nameInput = document.getElementById('new-role-name');
  const name = nameInput.value.trim();
  
  if (!name) {
    showAlert('Please enter a role name', 'error');
    return;
  }
  
  try {
    const response = await fetch(`${API_BASE}/admin/roles`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ name })
    });
    
    if (!response.ok) {
      throw new Error('Failed to add role');
    }
    
    showAlert('Role added successfully');
    nameInput.value = '';
    loadRoles();
  } catch (error) {
    showAlert(error.message, 'error');
  }
}

async function deleteRole(roleId) {
  if (!confirm('Are you sure you want to delete this role?')) {
    return;
  }
  
  try {
    const response = await fetch(`${API_BASE}/admin/roles/${roleId}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    
    if (!response.ok) {
      throw new Error('Failed to delete role');
    }
    
    showAlert('Role deleted successfully');
    loadRoles();
  } catch (error) {
    showAlert(error.message, 'error');
  }
}

// Specializations Functions
async function loadSpecializations() {
  try {
    const response = await fetch(`${API_BASE}/admin/specializations`, {
      headers: getAuthHeaders()
    });
    
    if (!response.ok) {
      throw new Error('Failed to load specializations');
    }
    
    const specs = await response.json();
    const container = document.getElementById('specs-list');
    
    container.innerHTML = specs.map(spec => `
      <li class="list-group-item">
        <span>${escapeHtml(spec.name)} (ID: ${spec.id})</span>
        <div>
          <button class="btn btn-danger" onclick="deleteSpecialization(${spec.id})">Delete</button>
        </div>
      </li>
    `).join('');
  } catch (error) {
    showAlert(error.message, 'error');
  }
}

async function addSpecialization() {
  const nameInput = document.getElementById('new-spec-name');
  const name = nameInput.value.trim();
  
  if (!name) {
    showAlert('Please enter a specialization name', 'error');
    return;
  }
  
  try {
    const response = await fetch(`${API_BASE}/admin/specializations`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ name })
    });
    
    if (!response.ok) {
      throw new Error('Failed to add specialization');
    }
    
    showAlert('Specialization added successfully');
    nameInput.value = '';
    loadSpecializations();
  } catch (error) {
    showAlert(error.message, 'error');
  }
}

async function deleteSpecialization(specId) {
  if (!confirm('Are you sure you want to delete this specialization?')) {
    return;
  }
  
  try {
    const response = await fetch(`${API_BASE}/admin/specializations/${specId}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    
    if (!response.ok) {
      throw new Error('Failed to delete specialization');
    }
    
    showAlert('Specialization deleted successfully');
    loadSpecializations();
  } catch (error) {
    showAlert(error.message, 'error');
  }
}

// Leave Types Functions
async function loadLeaveTypes() {
  try {
    const response = await fetch(`${API_BASE}/admin/leave-types`, {
      headers: getAuthHeaders()
    });
    
    if (!response.ok) {
      throw new Error('Failed to load leave types');
    }
    
    const leaveTypes = await response.json();
    const container = document.getElementById('leave-types-list');
    
    container.innerHTML = leaveTypes.map(lt => `
      <li class="list-group-item">
        <span>${escapeHtml(lt.name)} (ID: ${lt.id})</span>
        <div>
          <button class="btn btn-danger" onclick="deleteLeaveType(${lt.id})">Delete</button>
        </div>
      </li>
    `).join('');
  } catch (error) {
    showAlert(error.message, 'error');
  }
}

async function addLeaveType() {
  const nameInput = document.getElementById('new-leave-type-name');
  const name = nameInput.value.trim();
  
  if (!name) {
    showAlert('Please enter a leave type name', 'error');
    return;
  }
  
  try {
    const response = await fetch(`${API_BASE}/admin/leave-types`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ name })
    });
    
    if (!response.ok) {
      throw new Error('Failed to add leave type');
    }
    
    showAlert('Leave type added successfully');
    nameInput.value = '';
    loadLeaveTypes();
  } catch (error) {
    showAlert(error.message, 'error');
  }
}

async function deleteLeaveType(leaveTypeId) {
  if (!confirm('Are you sure you want to delete this leave type?')) {
    return;
  }
  
  try {
    const response = await fetch(`${API_BASE}/admin/leave-types/${leaveTypeId}`, {
      method: 'DELETE',
      headers: getAuthHeaders()
    });
    
    if (!response.ok) {
      throw new Error('Failed to delete leave type');
    }
    
    showAlert('Leave type deleted successfully');
    loadLeaveTypes();
  } catch (error) {
    showAlert(error.message, 'error');
  }
}

// Employee Functions
async function loadEmployees() {
  try {
    const response = await fetch(`${API_BASE}/admin/employees`, {
      headers: getAuthHeaders()
    });
    
    if (!response.ok) {
      throw new Error('Failed to load employees');
    }
    
    const employees = await response.json();
    const container = document.getElementById('employees-list');
    
    container.innerHTML = `
      <table style="width: 100%; margin-top: 15px; border-collapse: collapse;">
        <thead>
          <tr style="background: #f0f0f0;">
            <th style="padding: 10px; text-align: left; border: 1px solid #ddd;">ID</th>
            <th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Name</th>
            <th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Username</th>
            <th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Email</th>
            <th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Salary</th>
            <th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Status</th>
          </tr>
        </thead>
        <tbody>
          ${employees.map(emp => `
            <tr>
              <td style="padding: 10px; border: 1px solid #ddd;">${emp.id}</td>
              <td style="padding: 10px; border: 1px solid #ddd;">${escapeHtml(emp.name)}</td>
              <td style="padding: 10px; border: 1px solid #ddd;">${escapeHtml(emp.username)}</td>
              <td style="padding: 10px; border: 1px solid #ddd;">${escapeHtml(emp.email)}</td>
              <td style="padding: 10px; border: 1px solid #ddd;">${emp.curr_salary ? '$' + escapeHtml(emp.curr_salary.toString()) : 'N/A'}</td>
              <td style="padding: 10px; border: 1px solid #ddd;">${emp.status === 1 ? 'Active' : 'Inactive'}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    `;
  } catch (error) {
    showAlert(error.message, 'error');
  }
}

async function addEmployee() {
  const name = document.getElementById('emp-name').value.trim();
  const username = document.getElementById('emp-username').value.trim();
  const email = document.getElementById('emp-email').value.trim();
  const password = document.getElementById('emp-password').value;
  const salary = document.getElementById('emp-salary').value;
  const role = document.getElementById('emp-role').value;
  const specialization = document.getElementById('emp-specialization').value;
  const team = document.getElementById('emp-team').value;
  
  if (!name || !username || !email || !password || !salary) {
    showAlert('Please fill in all required fields', 'error');
    return;
  }
  
  if (parseFloat(salary) <= 0) {
    showAlert('Salary must be greater than 0', 'error');
    return;
  }
  
  const data = {
    name,
    username,
    email,
    password,
    curr_salary: parseFloat(salary),
    role: parseInt(role) || 1,
    primary_team_id: parseInt(team) || 1
  };
  
  if (specialization) {
    data.specialization = parseInt(specialization);
  }
  
  try {
    const response = await fetch(`${API_BASE}/admin/employees`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(data)
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to add employee');
    }
    
    showAlert('Employee added successfully');
    // Clear form
    document.getElementById('emp-name').value = '';
    document.getElementById('emp-username').value = '';
    document.getElementById('emp-email').value = '';
    document.getElementById('emp-password').value = '';
    document.getElementById('emp-salary').value = '';
    document.getElementById('emp-specialization').value = '';
    
    loadEmployees();
  } catch (error) {
    showAlert(error.message, 'error');
  }
}

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
  loadCompanySettings();
});
