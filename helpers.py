import requests
import random
import string
from config import BASE_URL

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def register_new_courier():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    response = requests.post(f"{BASE_URL}/courier", json=payload)

    if response.status_code == 201:
        return {
            "login": login,
            "password": password,
            "firstName": first_name,
            "id": response.json().get("id")
        }
    
    return None

def get_fake_credentials():
    login = generate_random_string(10)
    password = generate_random_string(10)
    return {
        "login": login,
        "password": password
    }