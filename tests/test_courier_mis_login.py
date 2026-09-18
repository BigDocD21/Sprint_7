import requests
import allure
from config import BASE_URL

class TestCourierAuthNegative:
    @allure.feature("Авторизация курьера")
    @allure.story("Негативные сценарии")
    @allure.title("Проверка ошибки при отсутствии обязательного поля 'login'")
    def test_courier_login_missing_field(self):
        with allure.step("Подготовка: формирование payload без обязательного поля 'login'"):
            payload = {
                "password": "any_password_123"
            }

        with allure.step("Действие: отправка запроса на авторизацию с неполными данными"):
            response = requests.post(f"{BASE_URL}/courier/login", json=payload)

        try:
            response_body = response.json()
            response_text = ""
        except ValueError:
            response_body = {}
            response_text = response.text

        assert response.status_code != 200, (
            f"Ожидался ошибочный статус (не 200), но получен статус {response.status_code}. "
            f"Тело ответа: {response_text}"
        )

        assert ("message" in response_body) or ("error" in response_body), (
            "В ответе отсутствует ожидаемое поле 'message' или 'error'. "
            f"Полученный ответ: {response_body}"
        )