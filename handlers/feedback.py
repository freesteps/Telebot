# handlers/feedback.py
from telebot import types
from handlers.base import BaseHandler
from utils.storage import set_state, STATE_MAIN_MENU
from config import ADMIN_CHAT_ID
from utils.logger import log_user_action

class FeedbackHandler(BaseHandler):
    def handle_feedback(self, message):
        user_id = message.chat.id
        username = message.from_user.username
        feedback = message.text

        self.bot.send_message(
            ADMIN_CHAT_ID,
            text=f"Новый отзыв/предложение от пользователя @{username} (ID: {user_id}):\n{feedback}"
        )
        self.bot.send_message(
            user_id,
            text="Спасибо за ваш отзыв! Мы ценим ваше мнение.",
            reply_markup=self.create_back_markup()
        )
        log_user_action(user_id, username, f"Оставил отзыв: {feedback}")
        set_state(user_id, STATE_MAIN_MENU)

    def create_back_markup(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back_button = types.KeyboardButton("🔙 Вернуться в главное меню")
        markup.add(back_button)
        return markup
