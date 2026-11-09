from src.shared.domain.entities.session import Session


class SessionViewmodel:
    refresh_token: str
    user_id: str

    def __init__(self, session: Session):
        self.refresh_token = session.refresh_token
        self.user_id = session.user_id

    def to_dict(self) -> dict:
        return {
            'refresh_token': self.refresh_token,
            'user_id': self.user_id
        }


class UpdateSessionViewmodel:
    session: SessionViewmodel

    def __init__(self, session: Session):
        self.session = SessionViewmodel(session)

    def to_dict(self) -> dict:
        return {
            'updated_session': self.session.to_dict(),
            'message': 'the session was updated'
        }