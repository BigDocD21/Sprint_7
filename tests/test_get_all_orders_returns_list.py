import requests
import allure
from config import BASE_URL

class TestOrdersListPositive:
    @allure.feature("Список заказов")
    @allure.story("Позитивные сценарии")
    @allure.title("Проверка возврата списка заказов")
    def test_get_all_orders_returns_list(self):
        with allure.step("Действие: отправка GET-запроса для получения списка заказов"):
            response = requests.get(f"{BASE_URL}/orders")

        data = response.json()
        orders_list = data["orders"]

        assert response.status_code == 200, (
            f"Ожидался статус 200, но получен статус {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        assert isinstance(orders_list, list), (
            f"Поле 'orders' не является списком. Получено: {type(orders_list)}"
        )

        assert len(orders_list) >= 0, (
            f"Список заказов имеет некорректную длину: {len(orders_list)}"
        )
