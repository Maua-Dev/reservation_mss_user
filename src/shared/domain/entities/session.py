import abc
import uuid

from src.shared.helpers.errors.domain_errors import EntityError


class Session(abc.ABC):
    refresh_token: str
    user_id: str

    def __init__(self, refresh_token: str, user_id: str):
        if not Session.validate_refresh_token(refresh_token):
            raise EntityError("refresh_token")
        self.refresh_token = refresh_token

        if not Session.validate_user_id(user_id):
            raise EntityError("user_id")
        self.user_id = user_id

    @staticmethod
    def validate_refresh_token(refresh_token: str) -> bool:
        if not isinstance(refresh_token, str) or not refresh_token:
            return False
        return True

    @staticmethod
    def validate_user_id(user_id: str) -> bool:
        if isinstance(user_id, str):
            try:
                uuid.UUID(user_id)
                return True
            except ValueError:
                return False

        return False

    def to_dict(self):
        return {
            "refresh_token": self.refresh_token,
            "user_id": self.user_id
        }