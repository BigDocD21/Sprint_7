import requests
import allure
from config import BASE_URL

class TestCourierCreationNegative:
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
        try:
            response_body = response.json()
        except ValueError:
            response_body = {}
        assert response.status_code != 201, (
            f"Ожидался статус ошибки (не 201), но получен статус {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        assert ("message" in response_body) or ("error" in response_body), (
            "В теле ответа отсутствует ожидаемое поле 'message' или 'error'. "
            f"Полученный ответ: {response_body}"
        )
