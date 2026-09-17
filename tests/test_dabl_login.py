import requests
import allure
from config import BASE_URL
from helpers import register_new_courier

@allure.feature("Создание курьера")
@allure.story("Негативные сценарии")
@allure.title("Проверка ошибки при создании курьера с дублирующимся логином")
def test_create_duplicate_courier():
    with allure.step("Подготовка: создание первого курьера для получения уникального логина"):
        first_courier = register_new_courier()
        assert first_courier is not None

    payload = {
        "login": first_courier["login"],
        "password": "another_password_123",
        "firstName": "Another Name"
    }

    with allure.step("Действие: попытка создания второго курьера с тем же логином"):
        response = requests.post(f"{BASE_URL}/courier", json=payload)

    with allure.step("Проверка: статус ответа не должен быть 201 (успех)"):
        assert response.status_code != 201

    with allure.step("Проверка: в теле ответа должно быть сообщение об ошибке"):
        response_body = response.json()
        assert "message" in response_body or "error" in response_body