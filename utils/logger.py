# utils/logger.py
import logging

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

logger = setup_logger()

def log_user_action(user_id, username, action):
    identifier = f"ID: {user_id}" if not username else f"@{username}"
    logger.info(f"{identifier} нажал {action}")
