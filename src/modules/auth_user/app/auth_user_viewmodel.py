from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class AuthUserViewmodel:
    user_id: str
    name: str
    email: str
    ra: str
    role: ROLE
    confirm_user: bool
    created: bool

    def __init__(self, user: User, created: bool):
        self.created = created

        self.user_id = user.user_id
        self.name = user.name
        self.email = user.email
        self.ra = user.ra
        self.role = user.role
        self.confirm_user = user.confirm_user

    def to_dict(self):
        return {
            'user': {
                'user_id': self.user_id,
                'name': self.name,
                'email': self.email,
                'ra': self.ra,
                'role': self.role.value,
                'confirm_user': self.confirm_user
            },
            'created': self.created,
            'message': "the user was created successfully" if self.created else "the user was authenticated successfully"
        }
