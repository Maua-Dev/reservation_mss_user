from abc import ABC, abstractmethod

from src.shared.domain.entities.session import Session


class ISessionRepository(ABC):

    @abstractmethod
    def create_session(self, session: Session) -> Session:
        
        pass

    @abstractmethod
    def get_session(self, user_id: str) -> Session:
      
        pass

    @abstractmethod
    def update_session(self, session: Session) -> Session:
      
        pass

    @abstractmethod
    def delete_session(self, user_id: str) -> Session:
    
        pass