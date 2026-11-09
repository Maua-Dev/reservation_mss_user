from src.shared.domain.entities.session import Session
from src.shared.domain.repositories.session_repository_interface import ISessionRepository


class UpdateSessionUsecase:
    repo: ISessionRepository

    def __init__(self, repo: ISessionRepository):
        self.repo = repo

    def __call__(self, user_id: str, new_refresh_token: str) -> Session:
        session = Session(refresh_token=new_refresh_token, user_id=user_id)

        return self.repo.update_session(session)