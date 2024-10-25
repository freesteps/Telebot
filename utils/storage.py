# utils/storage.py
import os
from datetime import datetime

# Константы состояний
STATE_MAIN_MENU = "main_menu"
STATE_ORDER = "order"
STATE_ORDER_DETAILS = "order_details"
STATE_TRACK_ORDER = "track_order"
STATE_FEEDBACK = "feedback"
STATE_CALCULATE_COST = "calculate_cost"
STATE_MAIN_INFO = "main_info"
STATE_DOWNLOAD_APP = "download_app"

# Хранилища данных пользователей
USER_STATES = {}
USER_ORDERS = {}
USER_PHOTOS = {}

# Путь к файлу для сохранения источников пользователей
FILE_PATH = "user_sources.txt"


def set_state(user_id, state):
    """Устанавливает текущее состояние пользователя."""
    USER_STATES[user_id] = state


def get_state(user_id, default_state):
    """Получает текущее состояние пользователя, если оно не установлено, возвращает состояние по умолчанию."""
    return USER_STATES.get(user_id, default_state)


def save_user_source(user_id, username, ref_source):
    """
    Сохраняет источник пользователя в файл.
    Если пользователь уже существует, обновляет его данные.
    """
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            pass  # Создаем файл, если его нет

    with open(FILE_PATH, "r+", encoding="utf-8") as file:
        lines = file.readlines()
        user_found = False
        for i, line in enumerate(lines):
            if line.strip().endswith(f", {user_id}"):
                user_found = True
                parts = line.split(", ")
                current_username = parts[0].split(":")[0].strip()
                if current_username != username:
                    current_source = parts[1].strip()
                    lines[i] = f"{username}: {timestamp}, {current_source}, {user_id}\n"
                break
        if not user_found:
            new_entry = f"{username}: {timestamp}, {ref_source}, {user_id}\n"
            lines.append(new_entry)
        file.seek(0)

