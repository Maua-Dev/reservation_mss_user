import abc
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.domain.enums.role_enum import ROLE

class User(abc.ABC):
    name: str
    email: str
    user_id : str
    ra: str
    role : ROLE 
    confirm_user : bool 

    def __init__(self, name: str, email: str, user_id : str, ra: str, role: ROLE, confirm_user: bool):
        if not User.validade_name(name):
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

        if type(confirm_user) != bool (confirm_user):
            raise EntityError("confirm_user")
        self.confirm_user = confirm_user





