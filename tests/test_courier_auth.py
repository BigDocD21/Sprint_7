import requests
import allure
from config import BASE_URL
from helpers import get_fake_credentials

class TestCourierAuth:
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
            f"Тело ответа: {response.text}"
        )

        has_error_field = ("message" in response_body) or ("error" in response_body)
        assert has_error_field, (
            "В теле ответа отсутствует ожидаемое поле 'message' или 'error'. "
            f"Полученный ответ: {response_body}"
        )

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

        response_body = response.json()

        assert response.status_code == 404, (
            f"Ожидался статус 404, но получен статус {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        assert "message" in response_body, (
            "В ответе отсутствует поле 'message'. "
            f"Полученный ответ: {response_body}"
        )

        assert response_body["message"] == "Учетная запись не найдена", (
            f"Неверный текст ошибки. Ожидалось 'Учетная запись не найдена', "
            f"получено: '{response_body.get('message')}'"
        )

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

        response_body = response.json()

        assert response.status_code != 200, (
            f"Ожидался ошибочный статус (не 200), но получен статус {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        has_error_field = ("message" in response_body) or ("error" in response_body)
        assert has_error_field, (
            "В ответе отсутствует ожидаемое поле 'message' или 'error'. "
            f"Полученный ответ: {response_body}"
        )
