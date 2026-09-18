import requests
import allure
from config import BASE_URL

class TestCourierCreationPositive:
    @allure.feature("Создание курьера")
    @allure.story("Позитивные сценарии")
    @allure.title("Проверка успешного создания курьера")
    def test_create_courier_success(self, created_courier):
        with allure.step("Подготовка: данные курьера получены из фикстуры"):
            courier = created_courier
        assert courier is not None, "Фикстура не вернула данные курьера"
        assert "login" in courier, "В данных курьера отсутствует логин"
        assert courier["login"] is not None, "Логин курьера пустой"
        payload = {
            "login": courier["login"],
            "password": courier["password"]
        }
        
        with allure.step("Действие: попытка авторизации созданного курьера (проверка существования)"):
            response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        assert response.status_code == 200, f"Не удалось залогиниться под созданным курьером. Статус: {response.status_code}"
        
        response_body = response.json()
        assert "id" in response_body, "При авторизации сервер вернул ID, это подтверждает существование курьера"
        assert response_body["id"] is not None, "ID курьера при авторизации не пустой"