from src.shared.domain.entities.session import Session
from src.shared.domain.repositories.session_repository_interface import ISessionRepository
from src.shared.helpers.errors.domain_errors import EntityError


class GetSessionUsecase:
    repo: ISessionRepository

    def __init__(self, repo: ISessionRepository):
        self.repo = repo

    def __call__(self, user_id: str) -> Session:
        if not Session.validate_user_id(user_id):
            raise EntityError("user_id")

        return self.repo.get_session(user_id)