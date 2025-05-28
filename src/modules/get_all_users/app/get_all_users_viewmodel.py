from typing import List
from src.shared.domain.entities.user import User


class UserViewModel:
    name: str
    email: str
    user_id: str
    ra: str
    role: str
    confirm_user: bool

    def __init__(self, user: User):
        self.name = user.name
        self.email = user.email
        self.user_id = user.user_id
        self.ra = user.ra
        self.role = user.role.value
        self.confirm_user = user.confirm_user

    def to_dict(self) -> User:
        return {
            'name': self.name,
            'email': self.email,
            'user_id': self.user_id,
            'ra': self.ra,
            'role': self.role,
            'confirm_user': self.confirm_user
        }

class GetAllUsersViewModel:
    def __init__(self, users: User):
        self.users_viewmodel = UserViewModel(users)

    def to_dict(self):
        return {    
            'users': self.users_viewmodel.to_dict(),
        }
    

class GetAllUsersViewModel:
    users: List[UserViewModel]

    def __init__(self, users: List[User]):
        self.users = [UserViewModel(user) for user in users]

    def to_dict(self) -> List[User]:
        return {
            'users': [user.to_dict() for user in self.users],
            'message': 'All users returned successfully'
        }
