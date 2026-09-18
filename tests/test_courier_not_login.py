import requests
import allure
from config import BASE_URL
from helpers import get_fake_credentials

class TestCourierCreationNegative:
    @allure.feature("Создание курьера")
    @allure.story("Негативные сценарии")
    @allure.title("Проверка ошибки при создании курьера без обязательного поля 'login'")
    def test_create_courier_missing_login(self):
        with allure.step("Подготовка: генерация данных и формирование payload без поля 'login'"):
            credentials = get_fake_credentials()

            payload = {
                "password": credentials["password"]
            }

        with allure.step("Действие: отправка запроса на создание курьера с неполными данными"):
            response = requests.post(f"{BASE_URL}/courier", json=payload)

        try:
            response_body = response.json()
            response_text = ""
        except ValueError:
            response_body = {}
            response_text = response.text

        assert response.status_code != 201, (
            f"Ожидался статус ошибки (не 201), но получен статус {response.status_code}. "
            f"Тело ответа: {response_text}"
        )

        assert ("message" in response_body) or ("error" in response_body), (
            "В ответе отсутствует ожидаемое поле 'message' или 'error'. "
            f"Полученный ответ: {response_body}"
        )
