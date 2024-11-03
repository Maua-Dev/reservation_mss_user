from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from typing import Optional

class UserViewModel:
    name: str
    email: str
    user_id: str
    ra: Optional[str] = None
    role: ROLE
    confirm_user: bool

    def __init__(self, user: User):
        self.name = user.name
        self.email = user.email
        self.user_id = user.user_id
        self.ra = user.ra
        self.role = user.role
        self.confirm_user = user.confirm_user

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "user_id": self.user_id,
            "ra": self.ra,
            "role": self.role.value if self.role else None,
            "confirm_user": self.confirm_user
        }
    
class GetUserViewModel(UserViewModel):
    user_viewmodel: UserViewModel

    def __init__(self, user: User):
        self.user_viewmodel = UserViewModel(user)

    def to_dict(self):
        return{
            "user": self.user_viewmodel.to_dict(),
            "message": "the user was retrieved"
        }
