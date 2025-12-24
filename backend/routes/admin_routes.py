from apiflask import APIBlueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, jsonify
from backend.models import db
from backend.models.company_settings import CompanySetting, Role, Specialization, LeaveType
from backend.models.employee import Employee

bp = APIBlueprint('admin', __name__, url_prefix='/admin')


def check_admin_role():
    """Check if current user has admin role (role_id=14)"""
    current_user_id = int(get_jwt_identity())
    user = Employee.query.get(current_user_id)
    if not user or user.role != 14:
        return False
    return True


# Company Settings endpoints
@bp.get('/settings')
@jwt_required()
def get_all_settings():
    """Get all company settings"""
    if not check_admin_role():
        return {"error": "Unauthorized. Admin access required."}, 403
    
    settings = CompanySetting.query.all()
    return jsonify([s.to_dict() for s in settings])


@bp.get('/settings/<string:key>')
@jwt_required()
def get_setting(key):
    """Get a specific company setting by key"""
    if not check_admin_role():
        return {"error": "Unauthorized. Admin access required."}, 403
    
    setting = CompanySetting.query.filter_by(key=key).first()
    if not setting:
        return {"error": "Setting not found"}, 404
    return setting.to_dict()


@bp.post('/settings')
@jwt_required()
def create_setting():
    """Create a new company setting"""
    if not check_admin_role():
        return {"error": "Unauthorized. Admin access required."}, 403
    
    data = request.get_json()
    if not data or 'key' not in data or 'value' not in data:
        return {"error": "Missing required fields: key and value"}, 400
    
    # Check if setting already exists
    existing = CompanySetting.query.filter_by(key=data['key']).first()
    if existing:
        return {"error": "Setting with this key already exists"}, 400
    
    setting = CompanySetting(
        key=data['key'],
        value=data['value'],
        description=data.get('description', '')
    )
    db.session.add(setting)
    db.session.commit()
    
    return setting.to_dict(), 201


@bp.put('/settings/<int:setting_id>')
@jwt_required()
def update_setting(setting_id):
    """Update a company setting"""
    if not check_admin_role():
        return {"error": "Unauthorized. Admin access required."}, 403
    
    setting = CompanySetting.query.get(setting_id)
    if not setting:
        return {"error": "Setting not found"}, 404
    
    data = request.get_json()
    if not data:
        return {"error": "No data provided"}, 400
    
    if 'value' in data:
        setting.value = data['value']
    if 'description' in data:
        setting.description = data['description']
    
    db.session.commit()
    return setting.to_dict()


@bp.delete('/settings/<int:setting_id>')
@jwt_required()
def delete_setting(setting_id):
    """Delete a company setting"""
    if not check_admin_role():
        return {"error": "Unauthorized. Admin access required."}, 403
    
    setting = CompanySetting.query.get(setting_id)
    if not setting:
        return {"error": "Setting not found"}, 404
    
    db.session.delete(setting)
    db.session.commit()
    return {"message": "Setting deleted successfully"}


# Role endpoints
@bp.get('/roles')
@jwt_required()
def get_all_roles():
    """Get all roles"""
    if not check_admin_role():
        return {"error": "Unauthorized. Admin access required."}, 403
    
    roles = Role.query.all()
    return jsonify([r.to_dict() for r in roles])


@bp.post('/roles')
@jwt_required()
def create_role():
    """Create a new role"""
    if not check_admin_role():
        return {"error": "Unauthorized. Admin access required."}, 403
    
    data = request.get_json()
    if not data or 'name' not in data:
        return {"error": "Missing required field: name"}, 400
    
    role = Role(name=data['name'])
    db.session.add(role)
    db.session.commit()
    
    return role.to_dict(), 201


@bp.put('/roles/<int:role_id>')
@jwt_required()
def update_role(role_id):
    """Update a role"""
    if not check_admin_role():
        return {"error": "Unauthorized. Admin access required."}, 403
    
    role = Role.query.get(role_id)
    if not role:
        return {"error": "Role not found"}, 404
    
    data = request.get_json()
    if not data or 'name' not in data:
        return {"error": "Missing required field: name"}, 400
    
    role.name = data['name']
    db.session.commit()
    return role.to_dict()


@bp.delete('/roles/<int:role_id>')
@jwt_required()
def delete_role(role_id):
    """Delete a role"""
    if not check_admin_role():
        return {"error": "Unauthorized. Admin access required."}, 403
    
    role = Role.query.get(role_id)
    if not role:
        return {"error": "Role not found"}, 404
    
    db.session.delete(role)
    db.session.commit()
    return {"message": "Role deleted successfully"}


# Specialization endpoints
@bp.get('/specializations')
@jwt_required()
def get_all_specializations():
    """Get all specializations"""
    if not check_admin_role():
        return {"error": "Unauthorized. Admin access required."}, 403
    
    specs = Specialization.query.all()
    return jsonify([s.to_dict() for s in specs])


@bp.post('/specializations')
@jwt_required()
def create_specialization():
    """Create a new specialization"""
    if not check_admin_role():
        return {"error": "Unauthorized. Admin access required."}, 403
    
    data = request.get_json()
    if not data or 'name' not in data:
        return {"error": "Missing required field: name"}, 400
    
    spec = Specialization(name=data['name'])
    db.session.add(spec)
    db.session.commit()
    
    return spec.to_dict(), 201


@bp.put('/specializations/<int:spec_id>')
@jwt_required()
def update_specialization(spec_id):
    """Update a specialization"""
    if not check_admin_role():
        return {"error": "Unauthorized. Admin access required."}, 403
    
    spec = Specialization.query.get(spec_id)
    if not spec:
        return {"error": "Specialization not found"}, 404
    
    data = request.get_json()
    if not data or 'name' not in data:
        return {"error": "Missing required field: name"}, 400
    
    spec.name = data['name']
    db.session.commit()
    return spec.to_dict()


@bp.delete('/specializations/<int:spec_id>')
@jwt_required()
def delete_specialization(spec_id):
    """Delete a specialization"""
    if not check_admin_role():
        return {"error": "Unauthorized. Admin access required."}, 403
    
    spec = Specialization.query.get(spec_id)
    if not spec:
        return {"error": "Specialization not found"}, 404
    
    db.session.delete(spec)
    db.session.commit()
    return {"message": "Specialization deleted successfully"}


# Leave Type endpoints
@bp.get('/leave-types')
@jwt_required()
def get_all_leave_types():
    """Get all leave types"""
    if not check_admin_role():
        return {"error": "Unauthorized. Admin access required."}, 403
    
    leave_types = LeaveType.query.all()
    return jsonify([lt.to_dict() for lt in leave_types])


@bp.post('/leave-types')
@jwt_required()
def create_leave_type():
    """Create a new leave type"""
    if not check_admin_role():
        return {"error": "Unauthorized. Admin access required."}, 403
    
    data = request.get_json()
    if not data or 'name' not in data:
        return {"error": "Missing required field: name"}, 400
    
    leave_type = LeaveType(name=data['name'])
    db.session.add(leave_type)
    db.session.commit()
    
    return leave_type.to_dict(), 201


@bp.put('/leave-types/<int:leave_type_id>')
@jwt_required()
def update_leave_type(leave_type_id):
    """Update a leave type"""
    if not check_admin_role():
        return {"error": "Unauthorized. Admin access required."}, 403
    
    leave_type = LeaveType.query.get(leave_type_id)
    if not leave_type:
        return {"error": "Leave type not found"}, 404
    
    data = request.get_json()
    if not data or 'name' not in data:
        return {"error": "Missing required field: name"}, 400
    
    leave_type.name = data['name']
    db.session.commit()
    return leave_type.to_dict()


@bp.delete('/leave-types/<int:leave_type_id>')
@jwt_required()
def delete_leave_type(leave_type_id):
    """Delete a leave type"""
    if not check_admin_role():
        return {"error": "Unauthorized. Admin access required."}, 403
    
    leave_type = LeaveType.query.get(leave_type_id)
    if not leave_type:
        return {"error": "Leave type not found"}, 404
    
    db.session.delete(leave_type)
    db.session.commit()
    return {"message": "Leave type deleted successfully"}


# Employee Management endpoints
@bp.get('/employees')
@jwt_required()
def get_all_employees():
    """Get all employees"""
    if not check_admin_role():
        return {"error": "Unauthorized. Admin access required."}, 403
    
    employees = Employee.query.all()
    return jsonify([e.to_dict() for e in employees])


@bp.post('/employees')
@jwt_required()
def create_employee():
    """Create a new employee"""
    if not check_admin_role():
        return {"error": "Unauthorized. Admin access required."}, 403
    
    data = request.get_json()
    if not data:
        return {"error": "No data provided"}, 400
    
    # Validate required fields
    required_fields = ['name', 'username', 'email', 'password', 'curr_salary']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return {"error": f"Missing required fields: {', '.join(missing_fields)}"}, 400
    
    # Check if username already exists
    existing = Employee.query.filter_by(username=data['username']).first()
    if existing:
        return {"error": "Username already exists"}, 400
    
    # Hash the password
    from backend.services.auth_service import hash_password
    hashed_password = hash_password(data['password'])
    
    employee = Employee(
        name=data['name'],
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        curr_salary=data['curr_salary'],
        role=data.get('role', 1),
        specialization=data.get('specialization'),
        primary_team_id=data.get('primary_team_id', 1),
        status=data.get('status', 1)
    )
    
    db.session.add(employee)
    db.session.commit()
    
    return employee.to_dict(), 201


@bp.put('/employees/<int:employee_id>')
@jwt_required()
def update_employee(employee_id):
    """Update an employee"""
    if not check_admin_role():
        return {"error": "Unauthorized. Admin access required."}, 403
    
    employee = Employee.query.get(employee_id)
    if not employee:
        return {"error": "Employee not found"}, 404
    
    data = request.get_json()
    if not data:
        return {"error": "No data provided"}, 400
    
    # Update allowed fields
    if 'name' in data:
        employee.name = data['name']
    if 'email' in data:
        employee.email = data['email']
    if 'role' in data:
        employee.role = data['role']
    if 'specialization' in data:
        employee.specialization = data['specialization']
    if 'primary_team_id' in data:
        employee.primary_team_id = data['primary_team_id']
    if 'status' in data:
        employee.status = data['status']
    if 'curr_salary' in data:
        employee.curr_salary = data['curr_salary']
    if 'password' in data:
        from backend.services.auth_service import hash_password
        employee.password = hash_password(data['password'])
    
    db.session.commit()
    return employee.to_dict()


@bp.delete('/employees/<int:employee_id>')
@jwt_required()
def delete_employee(employee_id):
    """Delete an employee (soft delete by setting status to 0)"""
    if not check_admin_role():
        return {"error": "Unauthorized. Admin access required."}, 403
    
    employee = Employee.query.get(employee_id)
    if not employee:
        return {"error": "Employee not found"}, 404
    
    # Soft delete by setting status to 0
    employee.status = 0
    db.session.commit()
    return {"message": "Employee deleted successfully"}
