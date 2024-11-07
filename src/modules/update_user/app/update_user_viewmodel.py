from typing import Optional
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class UserViewModel:
    user_id: str
    role: ROLE
    confirm_user: bool

    def __init__(self, user: User):
        self.user_id = user.user_id
        self.role = user.role
        self.confirm_user = user.confirm_user

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'role': self.role.value,
            'confirm_user': self.confirm_user
        }

class UpdateUserViewModel:
    def __init__(self, user: User):
        self.user = UserViewModel(user)

    def to_dict(self) -> dict:
        return {
            'updated_user': self.user.to_dict(),
            'message': 'User information was updated successfully.'
        }
