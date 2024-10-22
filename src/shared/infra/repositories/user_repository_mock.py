from typing import List, Optional
from shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.domain.repositories.user_repository_interface import IUserRepository

class UserRepositoryMock(IUserRepository):
    users_list: List[User]

    def __init__(self):
        self.users_list = [
            User(
                name="Rodas Rodas", 
                email="rodas@gmail.com", 
                user_id="93bc6ada-c0d1-7054-26ab-e17414c48ae3", 
                ra=None,
                role=RoleEnum.ADMIN, 
                confirm_user=True
            ),
            User(
                name="Rubio Rosa", 
                email="26.96379-5@maua.br",
                user_id="93bc6ada-c0d1-7054-26ab-e17414c48ae5",
                ra="26.96379-5",
                role=RoleEnum.ADMIN,
                confirm_user=False             
            ),
            User(
                name="Leo Iorio", 
                email="29.91279-6@maua.br", 
                user_id="93bc6ada-c0d1-7054-26ab-e17414c98ae4", 
                ra="29.91279-6",
                role=RoleEnum.STUDENT, 
                confirm_user=True
            ),
            User(
                name="Giovanna Ehobeckas",
                email="gi@hotmail.com",
                user_id="93bc6ada-c0d1-7054-26ab-e17454c48ae6",
                ra=None,
                role=RoleEnum.PROFESSOR,
                confirm_user=True
            ),
            User(
                name ="Vini Berti",
                email="berti@gmail.com",
                user_id="93bc6ada-c0d1-8754-26ab-e17414c48ae7",
                ra=None,
                role=RoleEnum.PROFESSOR,
                confirm_user=False
            ),
            User(
                name ="Gustavo Gus",
                email="timão@gmail.com",
                user_id="77bc6ada-c0d1-8754-26ab-e17414c48ae8",
                ra=None,
                role=RoleEnum.ADMIN,
                confirm_user=False
            ),
            User(
                name="Relâmpago Marquinhos",
                email="12.12345-8@maua.br",
                user_id="93bc6ada-c0e1-7054-26ab-e17414c48ae9",
                ra="12.12345-8",
                role=RoleEnum.PROFESSOR,
                confirm_user=False
            ),
            User(
                name="Bart Simpson", 
                email="springfield@gmail.com", 
                user_id="93bc6ada-c0d1-7054-26ab-e17414c98ag7", 
                ra="29.89779-6",
                role=RoleEnum.STUDENT, 
                confirm_user=False
            )
]

    def create_user(self, user: User) -> User:
        self.users_list.append(user)
        return user
    
    def get_user_by_id(self, user_id: str) -> User:
        for user in self.users_list:
            if user.user_id == user_id:
                return user
        return None
    
    def update_user_by_id(self, user_id: str, new_name : Optional[str] = None, new_email : Optional[str] = None, new_ra : Optional[str] = None):
        user_to_update = self.get_user_by_id(user_id)

        if user_to_update is None:
            return None 
        
        if new_name is not None:
            user_to_update.name = new_name
        
        if new_email is not None:
            user_to_update.email = new_email

        if new_ra is not None:
            user_to_update.ra = new_ra

        return user_to_update

    def delete_user_by_id(self, user_id: str) -> Optional[User]:
        for user in self.users_list:
            if user.user_id == user_id:
                self.users_list.remove(user)
                return user
        return None