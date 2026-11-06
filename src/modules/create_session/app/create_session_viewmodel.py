from src.shared.domain.entities.session import Session


class CreateSessionViewmodel:
    refresh_token: str
    user_id: str

    def __init__(self, session: Session):
        self.refresh_token = session.refresh_token
        self.user_id = session.user_id

    def to_dict(self):
        return {
            'session': {
                'refresh_token': self.refresh_token,
                'user_id': self.user_id
            },
            'message': "the session was created successfully"
        }