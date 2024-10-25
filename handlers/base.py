# handlers/base.py
from telebot import TeleBot, types
from utils.logger import log_user_action
from utils.storage import set_state, get_state
from config import REF_SOURCES

class BaseHandler:
    def __init__(self, bot: TeleBot):
        self.bot = bot

    def get_user_identifier(self, message):
        return message.from_user.username if message.from_user.username else message.chat.id
