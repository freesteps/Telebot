# utils/logger.py
import logging

# Настройка логирования
logger = logging.getLogger("bot_logger")
logger.setLevel(logging.INFO)

# Создание консольного обработчика
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Создание форматтера и добавление его к обработчику
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# Добавление обработчика к логгеру
logger.addHandler(ch)

def log_user_action(user_id, username, action):
    logger.info(f"@{username} (ID: {user_id}) - {action}")
