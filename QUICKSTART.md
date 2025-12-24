# Quick Start Guide - Admin Settings Feature

## 🚀 What Was Built

A complete admin configuration panel for managing company-wide settings, roles, specializations, leave types, and employees with mandatory salary tracking.

## 📁 Files Added

### Backend (5 files)
```
backend/
├── models/company_settings.py      # New models for settings, roles, specs, leave types
├── routes/admin_routes.py          # 20+ admin API endpoints
├── migrate_db.py                   # Database migration script
└── services/auth_service.py        # Updated with hash_password function
```

### Frontend (2 files)
```
Frontend/src/
├── html/views/admin/settings.html  # Admin settings page UI
└── assets/js/admin-settings.js     # API integration & form handling
```

### Documentation (3 files)
```
├── ADMIN_SETTINGS_FEATURE.md       # Complete feature documentation
├── IMPLEMENTATION_SUMMARY.md       # Implementation details
├── test_admin_settings.py          # Validation tests
└── .gitignore                      # Python cache exclusions
```

## 🎯 Key Features

### 1. Company Settings (4 default settings)
- **WFH Deduction**: 10% salary deduction for work from home
- **OT Addition**: 15% hourly bonus for overtime
- **Unpaid Leaves**: 5 default unpaid/medical leaves
- **Paid Default**: Leaves are paid by default

### 2. Entity Management
- **Roles**: Add/edit/delete role definitions
- **Specializations**: Manage employee specializations
- **Leave Types**: Configure available leave types

### 3. Employee Management
- **Mandatory Salary**: All new employees must have curr_salary
- **Full CRUD**: Create, read, update, delete operations
- **Soft Deletes**: Employees deactivated, not permanently removed

## 🔐 Security

- ✅ JWT Authentication required
- ✅ Admin role authorization (role_id = 14)
- ✅ Password hashing with werkzeug
- ✅ XSS protection via HTML escaping
- ✅ Input validation on all endpoints

## 📊 Database Changes

### New Table: company_settings
```sql
CREATE TABLE company_settings (
    id INTEGER PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value VARCHAR(500),
    description VARCHAR(255),
    created_at DATETIME,
    updated_at DATETIME
)
```

### Modified Table: Employee
```sql
ALTER TABLE Employee 
ADD COLUMN curr_salary DECIMAL(10, 2) DEFAULT 0.00
```

## 🛠️ How to Deploy

### Step 1: Run Migration
```bash
cd backend
python migrate_db.py
```

Expected output:
```
Adding curr_salary column to Employee table...
curr_salary column added successfully.
company_settings table created/verified.
Default setting 'wfh_salary_deduction_percent' added.
Default setting 'ot_salary_addition_percent' added.
Default setting 'default_unpaid_leaves' added.
Default setting 'leave_paid_by_default' added.
Migration completed successfully!
```

### Step 2: Verify Database
```bash
python test_admin_settings.py
```

Expected output:
```
✓ Employee table has curr_salary column
✓ company_settings table exists
✓ company_settings has 4 settings
```

### Step 3: Access Admin Panel
1. Start your Flask backend
2. Log in as admin (role_id = 14)
3. Navigate to: `/html/views/admin/settings.html`

## 📡 API Endpoints

### Company Settings
```
GET    /admin/settings           # List all
GET    /admin/settings/<key>     # Get one
POST   /admin/settings           # Create
PUT    /admin/settings/<id>      # Update
DELETE /admin/settings/<id>      # Delete
```

### Roles
```
GET    /admin/roles              # List all
POST   /admin/roles              # Create
PUT    /admin/roles/<id>         # Update
DELETE /admin/roles/<id>         # Delete
```

### Specializations
```
GET    /admin/specializations    # List all
POST   /admin/specializations    # Create
PUT    /admin/specializations/<id> # Update
DELETE /admin/specializations/<id> # Delete
```

### Leave Types
```
GET    /admin/leave-types        # List all
POST   /admin/leave-types        # Create
PUT    /admin/leave-types/<id>   # Update
DELETE /admin/leave-types/<id>   # Delete
```

### Employees
```
GET    /admin/employees          # List all (with salary)
POST   /admin/employees          # Create (salary required)
PUT    /admin/employees/<id>     # Update
DELETE /admin/employees/<id>     # Soft delete
```

## 💡 Usage Examples

### Create Employee with Salary (Required)
```bash
curl -X POST http://localhost:5000/admin/employees \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepass123",
    "curr_salary": 60000.00,
    "role": 1,
    "specialization": 2,
    "primary_team_id": 1
  }'
```

### Update Company Setting
```bash
curl -X PUT http://localhost:5000/admin/settings/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "value": "15",
    "description": "Updated WFH deduction to 15%"
  }'
```

### Get All Settings
```bash
curl http://localhost:5000/admin/settings \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🎨 Frontend UI Features

### Tabbed Interface
1. **Company Settings Tab**: View and edit global configurations
2. **Roles Tab**: Manage role definitions
3. **Specializations Tab**: Manage specializations
4. **Leave Types Tab**: Manage leave type options
5. **Employees Tab**: Add employees with salary, view all employees

### Form Validation
- Required field validation
- Numeric validation for salary
- Email format validation
- Real-time error messages
- Success notifications

### User Experience
- One-click updates
- Confirmation dialogs for deletions
- Auto-refresh after operations
- Clean, responsive design
- Error handling with user-friendly messages

## 🧪 Testing

### Run Validation Tests
```bash
python test_admin_settings.py
```

### Manual Testing Checklist
- [ ] Admin can log in
- [ ] Settings page loads correctly
- [ ] Can update company settings
- [ ] Can add/edit/delete roles
- [ ] Can add/edit/delete specializations
- [ ] Can add/edit/delete leave types
- [ ] Can create employee with salary (required)
- [ ] Cannot create employee without salary
- [ ] Non-admin users cannot access endpoints

## 🐛 Troubleshooting

### "Unauthorized" Error
**Issue**: Getting 403 Unauthorized  
**Solution**: Ensure user has role_id = 14 (admin role)

### "Missing required fields" Error
**Issue**: Cannot create employee  
**Solution**: Ensure curr_salary is included in request

### Settings Not Saving
**Issue**: Updates don't persist  
**Solution**: Check database permissions and connection

### Frontend Not Loading
**Issue**: Blank page or errors  
**Solution**: 
1. Check backend server is running
2. Verify API_BASE URL in admin-settings.js
3. Check browser console for errors

## 📚 Documentation

- **Full Feature Docs**: `ADMIN_SETTINGS_FEATURE.md`
- **Implementation Details**: `IMPLEMENTATION_SUMMARY.md`
- **This Quick Start**: `QUICKSTART.md`

## ✅ Success Checklist

After deployment, verify:
- [x] Database migration completed
- [x] company_settings table exists with 4 rows
- [x] Employee table has curr_salary column
- [x] Admin endpoints return 200 (with valid token)
- [x] Admin endpoints return 403 (without admin role)
- [x] Frontend page loads correctly
- [x] Can create employee with salary
- [x] Settings updates persist across page reloads

## 🎉 You're Ready!

The admin settings feature is fully implemented and ready to use. Log in as an admin and start configuring your company settings!

---

**Need Help?** See `ADMIN_SETTINGS_FEATURE.md` for detailed documentation.
