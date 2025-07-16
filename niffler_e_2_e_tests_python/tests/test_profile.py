import uuid
from faker import Faker
from ..pages.profile_page import profile_page


class TestProfile:

    def test_ui_successful_filling_form(self, profile_page_update_name, envs):
        fake = Faker()
        profile_page.check_filling_form(fake.name())

    def test_ui_successful_sign_out(self, authenticated_user):
        username, _ = authenticated_user
        profile_page.check_sign_out()

    def test_ui_add_friend_invitation_send(self, register_new_user, authenticated_user):
        username, _ = authenticated_user
        profile_page.check_add_friends_invitation_send()

    def test_api_get_current_user(self, api_get_current_user):
        user_data = api_get_current_user()

        assert isinstance(user_data["id"], str)
        assert isinstance(user_data["username"], str)
        assert isinstance(user_data["fullname"], str)
        assert isinstance(user_data["currency"], str)

    def test_api_update_user_fullname(self, authenticated_user, api_update_user):
        username, _ = authenticated_user
        new_fullname = "Updated Name " + str(uuid.uuid4())[:8]  # Уникальное имя для каждого запуска

        updated_user = api_update_user({
            "username": username,  # Используем username для идентификации
            "fullname": new_fullname
        })

        assert updated_user["username"] == username, "Обновлены данные не того пользователя"
        assert updated_user["fullname"] == new_fullname, "Полное имя не обновилось"

    def test_api_get_all_users(self, api_get_all_users):
        users_data = api_get_all_users(page=0)

        assert isinstance(users_data, list)

        assert len(users_data) > 0

        first_user = users_data[0]
        assert "id" in first_user
        assert "username" in first_user
        assert "currency" in first_user

        users_with_friendship = [user for user in users_data if "friendshipStatus" in user]
        assert len(users_with_friendship) > 0

    def test_api_search_user_by_username(self, register_new_user, api_get_all_users):
        username, _ = register_new_user

        search_results = api_get_all_users(search_query=username)

        assert isinstance(search_results, list)

        assert len(search_results) > 0

        assert any(username.lower() in user["username"].lower() for user in search_results)
        assert any(user["username"] == username for user in search_results)
