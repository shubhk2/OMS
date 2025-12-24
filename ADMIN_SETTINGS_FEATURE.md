# Admin Configurable Settings Feature

## Overview
This feature allows administrators to configure company-specific settings through a dedicated admin panel. It includes both global configuration settings and management of database entities like roles, specializations, leave types, and employees.

## Database Changes

### 1. Employee Table
- **Added Column**: `curr_salary` (DECIMAL(10, 2))
- **Purpose**: Store the current salary of each employee
- **Required**: Yes, for new employee creation
- **Default**: 0.00 for existing employees

### 2. Company Settings Table
New table created to store global configuration settings:

```sql
CREATE TABLE company_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key VARCHAR(100) UNIQUE NOT NULL,
    value VARCHAR(500),
    description VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

#### Default Settings:
| Key | Default Value | Description |
|-----|---------------|-------------|
| `wfh_salary_deduction_percent` | 10 | Percentage deduction from salary for Work From Home |
| `ot_salary_addition_percent` | 15 | Percentage addition to hourly rate for Overtime per hour |
| `default_unpaid_leaves` | 5 | Default number of unpaid/medical leaves allowed |
| `leave_paid_by_default` | true | Whether leaves are paid by default (true/false) |

## Backend API Endpoints

All admin endpoints require JWT authentication with admin role (role_id = 14).

### Company Settings

- **GET** `/admin/settings` - Get all company settings
- **GET** `/admin/settings/<key>` - Get a specific setting by key
- **POST** `/admin/settings` - Create a new setting
  ```json
  {
    "key": "setting_key",
    "value": "setting_value",
    "description": "Setting description"
  }
  ```
- **PUT** `/admin/settings/<id>` - Update a setting
  ```json
  {
    "value": "new_value",
    "description": "Updated description"
  }
  ```
- **DELETE** `/admin/settings/<id>` - Delete a setting

### Roles

- **GET** `/admin/roles` - Get all roles
- **POST** `/admin/roles` - Create a new role
  ```json
  {
    "name": "Role Name"
  }
  ```
- **PUT** `/admin/roles/<id>` - Update a role
- **DELETE** `/admin/roles/<id>` - Delete a role

### Specializations

- **GET** `/admin/specializations` - Get all specializations
- **POST** `/admin/specializations` - Create a new specialization
  ```json
  {
    "name": "Specialization Name"
  }
  ```
- **PUT** `/admin/specializations/<id>` - Update a specialization
- **DELETE** `/admin/specializations/<id>` - Delete a specialization

### Leave Types

- **GET** `/admin/leave-types` - Get all leave types
- **POST** `/admin/leave-types` - Create a new leave type
  ```json
  {
    "name": "Leave Type Name"
  }
  ```
- **PUT** `/admin/leave-types/<id>` - Update a leave type
- **DELETE** `/admin/leave-types/<id>` - Delete a leave type

### Employee Management

- **GET** `/admin/employees` - Get all employees (including salary information)
- **POST** `/admin/employees` - Create a new employee
  ```json
  {
    "name": "Employee Name",
    "username": "username",
    "email": "email@example.com",
    "password": "password",
    "curr_salary": 50000.00,  // REQUIRED
    "role": 1,
    "specialization": 1,
    "primary_team_id": 1,
    "status": 1
  }
  ```
- **PUT** `/admin/employees/<id>` - Update an employee
- **DELETE** `/admin/employees/<id>` - Soft delete an employee (sets status to 0)

## Frontend Changes

### Admin Settings Page
**Location**: `/Frontend/src/html/views/admin/settings.html`

The admin settings page provides a tabbed interface for managing:

1. **Company Settings Tab**
   - View and update all company configuration settings
   - Each setting shows its description and current value
   - One-click update functionality

2. **Roles Tab**
   - List all existing roles
   - Add new roles
   - Delete roles

3. **Specializations Tab**
   - List all existing specializations
   - Add new specializations
   - Delete specializations

4. **Leave Types Tab**
   - List all existing leave types
   - Add new leave types
   - Delete leave types

5. **Employees Tab**
   - Add new employees with mandatory salary field
   - View all employees with their salary information
   - Employee table displays: ID, Name, Username, Email, Salary, Status

### JavaScript Module
**Location**: `/Frontend/src/assets/js/admin-settings.js`

Provides functionality for:
- Tab switching
- API calls to backend endpoints
- Form validation
- Alert notifications
- Dynamic list rendering

## Migration Script

**Location**: `/backend/migrate_db.py`

This script performs the following migrations:
1. Adds `curr_salary` column to Employee table
2. Creates `company_settings` table
3. Inserts default company settings
4. Creates trigger for `updated_at` column

To run the migration:
```bash
cd backend
python migrate_db.py
```

## Usage Instructions

### For Administrators

1. **Access the Settings Page**
   - Log in with admin credentials (role_id = 14)
   - Navigate to the Admin Settings page

2. **Configure Company Settings**
   - Switch to "Company Settings" tab
   - Update values as needed
   - Click "Update" to save changes

3. **Manage Roles/Specializations/Leave Types**
   - Switch to the appropriate tab
   - Add new items using the input field
   - Delete items using the delete button

4. **Add New Employees**
   - Switch to "Employees" tab
   - Fill in all required fields (including Current Salary)
   - Click "Add Employee"

### For Developers

#### Using Company Settings in Code

```python
from backend.models.company_settings import CompanySetting

# Get a specific setting
wfh_deduction = CompanySetting.query.filter_by(key='wfh_salary_deduction_percent').first()
if wfh_deduction:
    deduction_percent = float(wfh_deduction.value)
    
# Calculate salary with WFH deduction
adjusted_salary = base_salary * (1 - deduction_percent / 100)
```

#### Creating New Employees

```python
from backend.models.employee import Employee
from backend.services.auth_service import hash_password

employee = Employee(
    name="John Doe",
    username="johndoe",
    email="john@example.com",
    password=hash_password("password123"),
    curr_salary=60000.00,  # Required
    role=1,
    specialization=2,
    primary_team_id=1
)
db.session.add(employee)
db.session.commit()
```

## Security Considerations

1. **Authentication**: All admin endpoints require JWT authentication
2. **Authorization**: Only users with role_id = 14 (admin) can access admin endpoints
3. **Password Hashing**: Passwords are hashed using werkzeug's generate_password_hash
4. **Input Validation**: All inputs are validated before processing
5. **Soft Deletes**: Employees are soft-deleted (status = 0) to preserve data integrity

## Testing

### Backend Testing
```bash
# Run the validation script
python test_admin_settings.py
```

### Frontend Testing
1. Start the Flask backend server
2. Open the admin settings page in a browser
3. Test each tab's functionality
4. Verify API calls in browser developer tools

## Future Enhancements

Potential improvements for future versions:

1. **Approval Request Types**: Add management for approval request types
2. **Setting Validation**: Add validation rules for settings (min/max values, formats)
3. **Audit Log**: Track changes to settings and who made them
4. **Bulk Operations**: Import/export settings and entities
5. **Role-Based Settings**: Different settings for different roles
6. **Setting Categories**: Group settings by category
7. **Setting History**: Track historical values of settings
8. **Email Notifications**: Notify relevant parties when settings change

## Troubleshooting

### Common Issues

1. **"Unauthorized" Error**
   - Ensure you're logged in with an admin account (role_id = 14)
   - Check that JWT token is valid and not expired

2. **"Missing required fields" Error**
   - Ensure curr_salary is provided when creating new employees
   - Check that all required fields are filled

3. **Database Errors**
   - Run the migration script if tables don't exist
   - Check database permissions

4. **Frontend Not Loading**
   - Verify backend server is running
   - Check console for CORS errors
   - Ensure API_BASE URL is correct in admin-settings.js

## Files Modified/Created

### Backend
- `backend/models/employee.py` - Added curr_salary field
- `backend/models/company_settings.py` - New models for settings management
- `backend/routes/admin_routes.py` - New admin endpoints
- `backend/services/auth_service.py` - Added hash_password function
- `backend/app.py` - Registered admin blueprint
- `backend/migrate_db.py` - Database migration script
- `backend/office.db` - Updated database with new schema

### Frontend
- `Frontend/src/html/views/admin/settings.html` - Admin settings page
- `Frontend/src/assets/js/admin-settings.js` - Settings page functionality

### Documentation
- `test_admin_settings.py` - Validation test script
- `ADMIN_SETTINGS_FEATURE.md` - This documentation file
