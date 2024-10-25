# handlers/order.py
from telebot import types
from handlers.base import BaseHandler
from utils.storage import set_state, STATE_MAIN_MENU , STATE_ORDER_DETAILS, USER_PHOTOS, USER_ORDERS
from utils.logger import log_user_action
from config import ADMIN_CHAT_ID  # Импортируем ADMIN_CHAT_ID
import logging

logger = logging.getLogger("telegram_bot")

class OrderHandler(BaseHandler):
    def handle_order_photo(self, message):
        user_id = message.chat.id
        username = message.from_user.username

        if message.content_type == 'photo':
            file_id = message.photo[-1].file_id
            USER_PHOTOS[user_id] = file_id
            log_user_action(user_id, username, f"Отправил фото (file_id: {file_id})")
            self.bot.send_message(
                user_id,
                text="Фото получено. Пожалуйста, введите данные о заказе (размер, цена в юанях и прочие важные детали).",
                reply_markup=self.create_back_markup()
            )
            set_state(user_id, STATE_ORDER_DETAILS)
        else:
            self.bot.send_message(user_id, text="Пожалуйста, отправьте фото товара.", reply_markup=self.create_back_markup())

    def handle_order_details(self, message):
        user_id = message.chat.id
        username = message.from_user.username
        order_details = message.text

        USER_ORDERS[user_id] = order_details
        log_user_action(user_id, username, f"Предоставил данные о заказе: {order_details}")

        # Получаем file_id сохраненной фотографии
        file_id = USER_PHOTOS.get(user_id)
        if not file_id:
            self.bot.send_message(
                user_id,
                text="Ошибка: Не удалось найти фотографию вашего заказа. Пожалуйста, начните процесс заказа заново.",
                reply_markup=self.create_back_markup()
            )
            logger.error(f"ID: {user_id} (@{username}): Фотография заказа не найдена.")
            set_state(user_id, STATE_MAIN_MENU)
            return

        # Отправляем фотографию администратору
        try:
            self.bot.send_photo(
                ADMIN_CHAT_ID,
                photo=file_id,
                caption=f"📦 *Новый заказ от @{username}*\n\n📋 *Детали заказа:*\n{order_details}",
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Не удалось отправить заказ администратору: {e}")
            self.bot.send_message(
                user_id,
                text="Произошла ошибка при обработке вашего заказа. Пожалуйста, попробуйте позже.",
                reply_markup=self.create_back_markup()
            )
            set_state(user_id, STATE_MAIN_MENU)
            return

        self.bot.send_message(
            user_id,
            text="Ваш заказ принят! Мы свяжемся с вами для подтверждения. Спасибо!",
            reply_markup=self.create_back_markup()
        )
        set_state(user_id, STATE_MAIN_MENU)

    def create_back_markup(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back_button = types.KeyboardButton("🔙 Вернуться в главное меню")
        markup.add(back_button)
        return markup
