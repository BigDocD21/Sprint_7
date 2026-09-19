import random
import string
from config import BASE_URL

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def get_fake_credentials():
    login = generate_random_string(10)
    password = generate_random_string(10)
    return {
        "login": login,
        "password": password
    }
