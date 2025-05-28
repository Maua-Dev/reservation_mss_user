from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.dto.user_dynamo_dto import UserDynamoDTO


class TestUserDynamoDto:

    def test_user_dto_from_entity(self):
        user = User(
            user_id="93bc6adb-c0d1-7054-26ab-e17454c48ae9",
            email="kadine.professora@maua.br",
            ra=None,
            name="Kadine Palmeiras",
            role=ROLE.PROFESSOR,
            confirm_user=True
        )

        user_dto = UserDynamoDTO.from_entity(user)

        assert user_dto == UserDynamoDTO(
            user_id="93bc6adb-c0d1-7054-26ab-e17454c48ae9",
            email="kadine.professora@maua.br",
            ra=None,
            name="Kadine Palmeiras",
            role=ROLE.PROFESSOR,
            confirm_user=True
        )

    def test_user_dynamo_dto_to_dynamo(self):

        user_dto = UserDynamoDTO(
            user_id="93bc6adb-c0d1-7054-26ab-e17454c48ae9",
            email="kadine.professora@maua.br",
            ra=None,
            name="Kadine Palmeiras",
            role=ROLE.PROFESSOR,
            confirm_user=True
        )

        user_dynamo = user_dto.to_dynamo()

        assert user_dynamo == {
            "entity": "user",
            "user_id": "93bc6adb-c0d1-7054-26ab-e17454c48ae9",
            "email": "kadine.professora@maua.br",
            "ra": "None",
            "name": "Kadine Palmeiras",
            "role": ROLE.PROFESSOR.value,
            "confirm_user": True
        }

    def test_user_dynamo_dto_from_dynamo(self):

        user_dynamo = {
            "entity": "user",
            "user_id": "93bc6adb-c0d1-7054-26ab-e17454c48ae9",
            "email": "kadine.professora@maua.br",
            "ra": "None",
            "name": "Kadine Palmeiras",
            "role": ROLE.PROFESSOR.value,
            "confirm_user": True
        }

        user_dto = UserDynamoDTO.from_dynamo(user_dynamo)

        assert user_dto == UserDynamoDTO(
            user_id="93bc6adb-c0d1-7054-26ab-e17454c48ae9",
            email="kadine.professora@maua.br",
            ra=None,
            name="Kadine Palmeiras",
            role=ROLE.PROFESSOR,
            confirm_user=True
        )

    def test_user_dynamo_dto_to_entity(self):

        user_dto = UserDynamoDTO(
            user_id="93bc6adb-c0d1-7054-26ab-e17454c48ae9",
            email="kadine.professora@maua.br",
            ra=None,
            name="Kadine Palmeiras",
            role=ROLE.PROFESSOR,
            confirm_user=True
        )

        user = user_dto.to_entity()

        assert isinstance(user, User)

        assert user.__dict__ == User(
            user_id="93bc6adb-c0d1-7054-26ab-e17454c48ae9",
            email="kadine.professora@maua.br",
            ra=None,
            name="Kadine Palmeiras",
            role=ROLE.PROFESSOR,
            confirm_user=True
        ).__dict__

    def test_user_dynamo_dto_from_entity_to_dynamo_professor(self):

        user = User(
            user_id="93bc6adb-c0d1-7054-26ab-e17454c48ae9",
            email="kadine.professora@maua.br",
            ra=None,
            name="Kadine Palmeiras",
            role=ROLE.PROFESSOR,
            confirm_user=True
        )

        user_dynamo = UserDynamoDTO.from_entity(user).to_dynamo()

        assert user_dynamo == {
            "entity": "user",
            "user_id": "93bc6adb-c0d1-7054-26ab-e17454c48ae9",
            "email": "kadine.professora@maua.br",
            "ra": "None",
            "name": "Kadine Palmeiras",
            "role": ROLE.PROFESSOR.value,
            "confirm_user": True
        }

    def test_user_dynamo_dto_from_dynamo_to_entity_professor(self):

        user_dynamo = {
            "entity": "user",
            "user_id": "93bc6adb-c0d1-7054-26ab-e17454c48ae9",
            "email": "kadine.professora@maua.br",
            "ra": "None",
            "name": "Kadine Palmeiras",
            "role": ROLE.PROFESSOR.value,
            "confirm_user": True
        }

        user = UserDynamoDTO.from_dynamo(user_dynamo).to_entity()

        assert user.__dict__ == User(
            user_id="93bc6adb-c0d1-7054-26ab-e17454c48ae9",
            email="kadine.professora@maua.br",
            ra=None,
            name="Kadine Palmeiras",
            role=ROLE.PROFESSOR,
            confirm_user=True
        ).__dict__

    def test_user_dynamo_dto_from_entity_to_dynamo_student(self):

        user = User(
            user_id="93bc6adb-c0d1-7054-26ab-e17454c477e9",
            email="23.00847-4@maua.br",
            ra="23.00847-4",
            name="Memphis Depay",
            role=ROLE.STUDENT,
            confirm_user=True
        )

        user_dynamo = UserDynamoDTO.from_entity(user).to_dynamo()

        assert user_dynamo == {
            "entity": "user",
            "user_id": "93bc6adb-c0d1-7054-26ab-e17454c477e9",
            "email": "23.00847-4@maua.br",
            "ra": "23.00847-4",
            "name": "Memphis Depay",
            "role": ROLE.STUDENT.value,
            "confirm_user": True
        }

    def test_user_dynamo_dto_from_dynamo_to_entity_student(self):

        user_dynamo = {
            "entity": "user",
            "user_id": "93bc6adb-c0d1-7054-26ab-e17454c477e9",
            "email": "23.00847-4@maua.br",
            "ra": "23.00847-4",
            "name": "Memphis Depay",
            "role": ROLE.STUDENT.value,
            "confirm_user": True
        }

        user = UserDynamoDTO.from_dynamo(user_dynamo).to_entity()

        assert user.__dict__ == User(
            user_id="93bc6adb-c0d1-7054-26ab-e17454c477e9",
            email="23.00847-4@maua.br",
            ra="23.00847-4",
            name="Memphis Depay",
            role=ROLE.STUDENT,
            confirm_user=True
        ).__dict__

