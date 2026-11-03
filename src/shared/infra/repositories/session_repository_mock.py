from typing import List

from src.shared.domain.entities.session import Session
from src.shared.domain.repositories.session_repository_interface import ISessionRepository
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, NoItemsFound


class SessionRepositoryMock(ISessionRepository):
    sessions: List[Session]

    def __init__(self):
        self.sessions = [
            Session(
                refresh_token="refresh_token_1",
                user_id="00000000-0000-0000-0000-000000000001"
            ),
            Session(
                refresh_token="refresh_token_2",
                user_id="00000000-0000-0000-0000-000000000002"
            ),
        ]

    def create_session(self, session: Session) -> Session:
        for existing in self.sessions:
            if existing.user_id == session.user_id:
                raise DuplicatedItem("user_id")

        self.sessions.append(session)
        return session

    def get_session(self, user_id: str) -> Session:
        for session in self.sessions:
            if session.user_id == user_id:
                return session

        raise NoItemsFound("user_id")

    def update_session(self, session: Session) -> Session:
        for i, existing in enumerate(self.sessions):
            if existing.user_id == session.user_id:
                self.sessions[i] = session
                return session

        raise NoItemsFound("user_id")

    def delete_session(self, user_id: str) -> Session:
        for i, session in enumerate(self.sessions):
            if session.user_id == user_id:
                return self.sessions.pop(i)

        raise NoItemsFound("user_id")