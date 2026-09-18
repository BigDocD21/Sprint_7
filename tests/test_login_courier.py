import requests
import allure
from config import BASE_URL

class TestCourierAuthPositive:
    @allure.feature("Авторизация курьера")
    @allure.story("Позитивные сценарии")
    @allure.title("Проверка успешной авторизации курьера и получения ID")
    def test_courier_login_success(self, created_courier):
        with allure.step("Подготовка: получение данных тестового курьера из фикстуры"):
            courier = created_courier

        payload = {
            "login": courier["login"],
            "password": courier["password"]
        }

        with allure.step("Действие: отправка запроса на авторизацию"):
            response = requests.post(f"{BASE_URL}/courier/login", json=payload)

        response_data = response.json()

        assert response.status_code == 200, (
            f"Ожидался статус 200, но получен статус {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        assert "id" in response_data, (
            "В ответе от сервера отсутствует обязательное поле 'id'. "
            f"Полученный ответ: {response_data}"
        )

        assert response_data["id"] is not None, (
            "Поле 'id' присутствует, но оно пустое (None). "
            f"Данные курьера: {response_data}"
        )
