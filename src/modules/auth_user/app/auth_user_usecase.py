import re
from typing import Tuple

from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.domain.enums.role_enum import ROLE


class AuthUserUsecase:

    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def __call__(self,
                 user_id: str,
                 name: str,
                 email: str,
                 ) -> Tuple[User, bool]:

        if self.repo.get_user(user_id=user_id) is not None:
            return self.repo.get_user(user_id=user_id), False
        
        if email == "ceaf@maua.br":
            return self.repo.create_user(User(
                user_id=user_id,
                name=name,
                email=email,
                role=ROLE.ADMIN,
                confirm_user=True
            )), True

        ra_pattern = r'[0-9]+\.[0-9]+-[0-9]+@maua\.br'
        has_ra = re.match(ra_pattern, email)

        if not has_ra:
            # professor
            user = User(user_id=user_id, name=name, email=email, role=ROLE.PROFESSOR, confirm_user=False)

        else:
            # aluno
            ra_from_mail = re.search(ra_pattern, email).group(0)[:10]
            user = User(user_id=user_id, name=name, ra=ra_from_mail, email=email, role=ROLE.STUDENT, confirm_user=True)

        return self.repo.create_user(user), True
