import json

import pytest
from allure import step, epic, suite, title, id, tag
from faker import Faker

from niffler_e_2_e_tests_python.models.user import UserName


@epic("[KAFKA][niffler-auth]: Паблишинг сообщений в кафку")
@suite("[KAFKA][niffler-auth]: Паблишинг сообщений в кафку")
class TestAuthRegistrationKafkaTest:
        @id("600001")
        @title("KAFKA: Сообщение с пользователем публикуется в Kafka после успешной регистрации")
        @tag("KAFKA")
        def test_message_should_be_produced_to_kafka_after_successful_registration(self, register_new_user, kafka_connect):
                username = Faker().user_name()
                password = Faker().password(special_chars=False)

                topic_partitions = kafka_connect.subscribe_listen_new_offsets("users")

                result = register_new_user.register(username, password)
                assert result.status_code == 201

                event = kafka_connect.log_msg_and_json(topic_partitions)

                with step("Check that message from kafka exist"):
                        assert event != '' and event != b''

                with step("Check message content"):
                        UserName.model_validate(json.loads(event.decode('utf8')))
                        assert json.loads(event.decode('utf8'))['username'] == username

        def test_connect(self, kafka_connect):
                # Проверяем подключение
                if not kafka_connect.check_connection():
                        pytest.skip("Kafka is not available")

