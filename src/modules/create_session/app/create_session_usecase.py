from src.shared.domain.entities.session import Session
from src.shared.domain.repositories.session_repository_interface import ISessionRepository


class CreateSessionUsecase:
    repo: ISessionRepository

    def __init__(self, repo: ISessionRepository):
        self.repo = repo

    def __call__(self, user_id: str, refresh_token: str) -> Session:
        session = Session(refresh_token = refresh_token, user_id = user_id)

        return self.repo.create_session(session)