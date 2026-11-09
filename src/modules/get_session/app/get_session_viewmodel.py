from src.shared.domain.entities.session import Session


class SessionViewmodel:
    refresh_token: str
    user_id: str

    def __init__(self, session: Session):
        self.refresh_token = session.refresh_token
        self.user_id = session.user_id

    def to_dict(self):
        return {
            "refresh_token": self.refresh_token,
            "user_id": self.user_id
        }


class GetSessionViewmodel:
    session_viewmodel: SessionViewmodel

    def __init__(self, session: Session):
        self.session_viewmodel = SessionViewmodel(session)

    def to_dict(self):
        return {
            "session": self.session_viewmodel.to_dict(),
            "message": "the session was retrieved"
        }