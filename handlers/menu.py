# handlers/menu.py
from telebot import types
from handlers.base import BaseHandler
from utils.storage import set_state, STATE_MAIN_MENU
from utils.logger import log_user_action, logger  # Импортируем logger

class MenuHandler(BaseHandler):
    def main_menu(self, message):
        user_id = message.chat.id
        username = message.from_user.username

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [
            "🛒 Сделать заказ",
            "📦 Отследить заказ",
            "💬 Отзывы и предложения",
            "📈 Рассчитать стоимость",
            "ℹ️ Основная информация",
            "📄 Как происходит выкуп",
            "📲 Скачать Poizon"
        ]
        markup.add(*buttons)

        self.bot.send_message(
            user_id,
            text="Главное меню:",
            reply_markup=markup
        )
        log_user_action(user_id, username, "Показано главное меню")
        logger.info(f"Главное меню отправлено пользователю ID: {user_id}, username: {username}")
        set_state(user_id, STATE_MAIN_MENU)
