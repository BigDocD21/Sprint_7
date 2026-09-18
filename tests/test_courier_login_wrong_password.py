import requests
import allure
from config import BASE_URL

class TestCourierAuthNegative:
    @allure.feature("Авторизация курьера")
    @allure.story("Негативные сценарии")
    @allure.title("Проверка ошибки при неверном пароле")

    def test_courier_login_wrong_password(self, created_courier):
        with allure.step("Подготовка: получение данных валидного курьера из фикстуры"):
            login = created_courier["login"]
            wrong_password = "wrong_password_123"

        payload = {
            "login": login,
            "password": wrong_password
        }

        with allure.step("Действие: отправка запроса на авторизацию с неверным паролем"):
            response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        try:
            response_body = response.json()
        except ValueError:
            response_body = {}
            response_text = response.text
        else:
            response_text = ""
        assert response.status_code == 404, (
            f"Ожидался статус 404, но получен статус {response.status_code}. "
            f"Тело ответа: {response_text}"
        )

        assert "message" in response_body, (
            "В ответе отсутствует поле 'message'. "
            f"Полученный ответ: {response_body}"
        )

        assert response_body["message"] == "Учетная запись не найдена", (
            f"Неверный текст ошибки. Ожидалось 'Учетная запись не найдена', "
            f"получено: '{response_body.get('message')}'"
        )
