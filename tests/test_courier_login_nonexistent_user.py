import requests
import allure
from config import BASE_URL
from helpers import get_fake_credentials

class TestCourierAuthNegative:
    @allure.feature("Авторизация курьера")
    @allure.story("Негативные сценарии")
    @allure.title("Проверка ошибки при входе под несуществующим пользователем")
    def test_courier_login_nonexistent_user(self):
        with allure.step("Подготовка: генерация данных несуществующего пользователя"):
            credentials = get_fake_credentials()
            fake_login = credentials["login"]
            fake_password = credentials["password"]

        payload = {
            "login": fake_login,
            "password": fake_password
        }

        with allure.step("Действие: отправка POST-запроса на авторизацию"):
            response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        response_body = response.json()
        assert response.status_code != 200, (
            f"Ожидался ошибочный статус (не 200), но получен статус {response.status_code}. "
            f"Тело ответа: {response_body}"
        )

        has_error_field = ("message" in response_body) or ("error" in response_body)
        assert has_error_field, (
            "В теле ответа отсутствует ожидаемое поле 'message' или 'error'. "
            f"Полученный ответ: {response_body}"
        )
