from werkzeug.security import check_password_hash, generate_password_hash
from backend.models.employee import Employee
from logging import getLogger
logger = getLogger(__name__)


def hash_password(password: str) -> str:
    """Hash a password for storing."""
    return generate_password_hash(password)


def authenticate_user(username: str, password: str):
    """Return user dict if credentials are valid, else None."""
    # Try to find user by name or username
    user = Employee.query.filter(
        (Employee.username == username)
    ).first()

    logger.info(f"User {username} lookup result: {user.to_dict() if user else None}")

    if not user:
        return None

    if not user.password:
        raise RuntimeError("Account stored password missing — contact administrator")

    if not check_password_hash(user.password, password):
        return None

    return user.to_dict()

