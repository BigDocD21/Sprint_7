import requests
import allure
from config import BASE_URL
from helpers import get_fake_credentials

class TestCourierCreation:
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

        response_body = response.json()

        assert response.status_code != 201, (
            f"Ожидался статус ошибки (не 201), но получен статус {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        assert ("message" in response_body) or ("error" in response_body), (
            "В ответе отсутствует ожидаемое поле 'message' или 'error'. "
            f"Полученный ответ: {response_body}"
        )

    @allure.feature("Создание курьера")
    @allure.story("Негативные сценарии")
    @allure.title("Проверка ошибки при создании курьера без обязательного поля 'password'")
    def test_create_courier_missing_password(self):
        with allure.step("Подготовка: генерация данных и формирование payload без поля 'password'"):
            credentials = get_fake_credentials()
            payload = {
                "login": credentials["login"]
            }

        with allure.step("Действие: отправка запроса на создание курьера с неполными данными"):
            response = requests.post(f"{BASE_URL}/courier", json=payload)

        response_body = response.json()

        assert response.status_code != 201, (
            f"Ожидался статус ошибки (не 201), но получен статус {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        assert ("message" in response_body) or ("error" in response_body), (
            "В ответе отсутствует ожидаемое поле 'message' или 'error'. "
            f"Полученный ответ: {response_body}"
        )

    @allure.feature("Создание курьера")
    @allure.story("Негативные сценарии")
    @allure.title("Проверка ошибки при создании курьера с дублирующимся логином")
    def test_create_duplicate_courier(self, created_courier):
        with allure.step("Подготовка: получение логина существующего курьера из фикстуры"):
            existing_login = created_courier["login"]

        payload = {
            "login": existing_login,
            "password": "another_password_123",
            "firstName": "Another Name"
        }

        with allure.step("Действие: попытка создания второго курьера с тем же логином"):
            response = requests.post(f"{BASE_URL}/courier", json=payload)

        response_body = response.json()

        assert response.status_code != 201, (
            f"Ожидался статус ошибки (не 201), но получен статус {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        assert ("message" in response_body) or ("error" in response_body), (
            "В теле ответа отсутствует ожидаемое поле 'message' или 'error'. "
            f"Полученный ответ: {response_body}"
        )
