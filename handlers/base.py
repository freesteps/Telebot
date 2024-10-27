# handlers/base.py
from telebot import TeleBot

class BaseHandler:
    def __init__(self, bot: TeleBot):
        self.bot = bot

    def get_user_identifier(self, message):
        return message.from_user.username if message.from_user.username else message.chat.id
