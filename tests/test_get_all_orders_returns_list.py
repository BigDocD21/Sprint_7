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

        orders_list = None
        parse_error = None
        
        try:
            data = response.json()
            orders_list = data.get("orders")
        except ValueError as e:
            parse_error = f"Ошибка JSON: {e}"
        except KeyError as e:
            parse_error = f"Отсутствует ключ 'orders': {e}"

        assert response.status_code == 200, (
            f"Ожидался статус 200, но получен статус {response.status_code}. "
            f"Тело ответа: {response.text}"
        )

        assert orders_list is not None, (
            f"Не удалось извлечь список заказов. Ошибка: {parse_error}"
        )

        assert isinstance(orders_list, list), (
            f"Поле 'orders' не является списком. Получено: {type(orders_list)}"
        )
