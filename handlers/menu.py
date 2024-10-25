# handlers/menu.py
from telebot import types
from handlers.base import BaseHandler
from config import WORK_SCHEDULE
from utils.storage import set_state, STATE_MAIN_MENU
from utils.logger import log_user_action

class MenuHandler(BaseHandler):
    def main_menu(self, message):
        user_id = message.chat.id
        username = message.from_user.username

        log_user_action(user_id, username, "главное меню")
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
        markup.add(*[types.KeyboardButton(btn) for btn in buttons])
        self.bot.send_message(
            user_id,
            text="🏠 Главное меню.\nПожалуйста, выберите одну из опций.",
            reply_markup=markup
        )
        set_state(user_id, STATE_MAIN_MENU)
