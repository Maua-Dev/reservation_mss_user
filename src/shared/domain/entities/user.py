import abc
import re
from typing import Optional
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.domain.enums.role_enum import ROLE

class User(abc.ABC):
    name: str
    email: str
    user_id : str
    ra: Optional[str] = None
    role : ROLE 
    confirm_user : bool 

    def __init__(self, name: str, email: str, user_id : str, ra: str, role: ROLE, confirm_user: bool):
        if not User.validate_name(name):
            raise EntityError("name")
        self.name = name

        if not User.validate_email(email):
            raise EntityError("email")
        self.email = email

        if not User.validate_user_id(user_id):
            raise EntityError("user_id")
        self.user_id = user_id

        if not User.validate_ra(ra):
            raise EntityError("ra")
        self.ra = ra

        if not User.validate_role(role):
            raise EntityError("role")
        self.role = role

        if type(confirm_user) != bool (confirm_user,bool):
            raise EntityError("confirm_user")
        self.confirm_user = confirm_user


    @staticmethod
    def validate_name(name: str) -> bool:
        if not isinstance(name, str) or not name:
            return False
        return True

    @staticmethod
    def validate_email(email: str) -> bool:
        if not isinstance(email, str):
            return False
        
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    @staticmethod
    def validate_user_id(user_id: str) -> bool:
        if not isinstance(user_id, str) or not user_id:
            return False
        return True

    @staticmethod
    def validate_ra(ra: str) -> bool:
        if ra is None:
            return True 
        if not isinstance(ra, str) or not ra:
            return False
        ra_regex = r'^\d{2}\.\d{5}-\d$'
        if re.match(ra_regex, ra) is None:
            return False
        return True

    @staticmethod
    def validate_role(role: ROLE) -> bool:
        if not isinstance(role, ROLE):
            return False
        return True







