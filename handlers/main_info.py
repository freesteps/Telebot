# handlers/main_info.py
from telebot import types
from handlers.base import BaseHandler
from utils.storage import set_state, STATE_MAIN_INFO, STATE_MAIN_MENU
from utils.logger import log_user_action
from config import WORK_SCHEDULE

class MainInfoHandler(BaseHandler):
    def handle_main_info(self, message):
        user_id = message.chat.id
        username = message.from_user.username
        self.bot.send_message(
            user_id,
            text=f"{self.get_main_info_text()}\n\n{WORK_SCHEDULE}",
            reply_markup=self.create_info_markup()
        )
        log_user_action(user_id, username, "Основная информация")
        set_state(user_id, STATE_MAIN_MENU)

    def create_info_markup(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back_button = types.KeyboardButton("🔙 Вернуться в главное меню")
        purchase_button = types.KeyboardButton("📄 Как происходит выкуп")
        markup.add(purchase_button, back_button)
        return markup

    def get_main_info_text(self):
        return (
            "📦 Мы предлагаем услуги по выкупу и доставке товаров с Poizon на территорию РФ.\n"
            "⚙️ Рабочий процесс:\n"
            "1. Вы отправляете фото товара и указываете параметры (размер, цена).\n"
            "2. Мы оформляем заказ и высылаем вам подтверждение.\n"
            "3. Вы оплачиваете заказ и доставку.\n"
            "4. Мы доставляем товар в течение 30 или более (в худшем случае) рабочих дней через СДЭК.\n"
            "5. После оформления заказа вам потребуется заполнить паспортные данные на сайте СДЭК по инструкции, которую предоставит администратор."
        )

    def get_purchase_info_text(self):
        return (
            "📄 Процесс выкупа:\n"
            "1. Вы отправляете нам фото и параметры товара.\n"
            "2. Мы проверяем наличие и цену на Poizon.\n"
            "3. После подтверждения вы оплачиваете заказ.\n"
            "4. Мы выкупаем товар и организуем его доставку через СДЭК.\n"
            "5. После отправки заявки с вами свяжется администратор для дальнейших инструкций. Вам потребуется заполнить паспортные данные на сайте СДЭК."
        )
