from typing import Optional
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE


class UserDynamoDTO:
    user_id: str
    email: str
    ra: str
    name: str
    role: ROLE
    confirm_user = bool

    def __init__(self,
                 user_id: str,
                 email: str,
                 ra: str,
                 name: str,
                 role: ROLE,
                 confirm_user: bool):

        self.user_id = user_id
        self.email = email
        self.ra = ra
        self.name = name
        self.role = role
        self.confirm_user = confirm_user

    @staticmethod
    def from_entity(user: User) -> "UserDynamoDTO":
        """
        Parse data from User to UserDynamoDTO
        """
        return UserDynamoDTO(
            user_id = user.user_id,
            email = user.email,
            ra = user.ra,
            name = user.name,
            role = user.role,
            confirm_user = user.confirm_user
        )

    def to_dynamo(self) -> dict:
        """
        Parse data from UserDynamoDTO to dict
        """
        data = {
            "entity": "user",
            "user_id": self.user_id,
            "email": self.email,
            "ra": self.ra,
            "name": self.user_id,
            "role": self.role.value,
            "confirm_user": self.confirm_user
        }

        return data

    @staticmethod
    def from_dynamo(user_data: dict) -> "UserDynamoDTO":
        """
        Parse data from DynamoDB to UserDynamoDTO
        @param user_data: dict from DynamoDB
        """
        return UserDynamoDTO(
            user_id=str(user_data["user_id"]),
            email=str(user_data["email"]),
            ra=str(user_data["ra"]),
            name=str(user_data["name"]),
            role=next((role for role in ROLE if role.value == user_data["role"]), ROLE.STUDENT),
            confirm_user=user_data["confirm_user"]
        )

    def to_entity(self) -> User:
        """
        Parse data from UserDynamoDTO to User
        """
        return User(
            user_id=self.user_id,
            email=self.email,
            ra=self.ra,
            name=self.name,
            role=self.role,
            confirm_user=self.confirm_user
        )

    def __repr__(self):
        return f"UserDynamoDto(user_id={self.user_id}, email={self.email}, ra={self.ra}, name={self.name}, role={self.role.value}, confirm_user={self.confirm_user})"

    def __eq__(self, other):
        return self.__dict__ == other.__dict__