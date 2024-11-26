import random
import string


def generate_username(name):
    first_word = name.split()[0].lower().replace(",", "")
    random_digits = ''.join(random.choices(string.digits, k=5))
    return f"{first_word}_{random_digits}"
