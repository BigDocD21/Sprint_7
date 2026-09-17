import requests
import allure
from config import BASE_URL

@allure.feature("Авторизация курьера")
@allure.story("Негативные сценарии")
@allure.title("Проверка ошибки при отсутствии обязательного поля (login)")
def test_courier_login_missing_field():
    with allure.step("Подготовка: формирование payload без обязательного поля 'login'"):
        payload = {
            "password": "any_password_123"
        }

    with allure.step("Действие: отправка запроса на авторизацию"):
        response = requests.post(f"{BASE_URL}/courier/login", json=payload)

    with allure.step("Проверка статуса ответа (должен быть не 200)"):
        assert response.status_code != 200, f"Ожидалась ошибка валидации, но получен статус {response.status_code}"

    with allure.step("Проверка тела ответа на наличие сообщения об ошибке"):
        response_body = response.json()
        assert "message" in response_body or "error" in response_body