# handlers/calculate.py
from telebot import types
from handlers.base import BaseHandler
from utils.storage import set_state, STATE_CALCULATE_COST
from config import CURRENCY_RATES
from utils.logger import log_user_action

class CalculateHandler(BaseHandler):
    def handle_calculate_cost(self, message):
        user_id = message.chat.id
        username = message.from_user.username

        try:
            amount_cny = float(message.text)
            if amount_cny < 100:
                raise ValueError("Минимальная сумма 100 CNY.")
            if amount_cny <= 1000:
                cost_rub = amount_cny * CURRENCY_RATES['100_1000']
            elif amount_cny <= 8000:
                cost_rub = amount_cny * CURRENCY_RATES['1001_8000']
            else:
                cost_rub = amount_cny * CURRENCY_RATES['8001_20000']
            self.bot.send_message(
                user_id,
                text=f"Примерная стоимость: {cost_rub:.2f} RUB.",
                reply_markup=self.create_back_markup()
            )
            log_user_action(user_id, username, f"Рассчитал стоимость: {amount_cny} CNY = {cost_rub:.2f} RUB")
        except ValueError as e:
            self.bot.send_message(user_id, text=str(e), reply_markup=self.create_back_markup())
            log_user_action(user_id, username, "Ошибка при расчете стоимости")

    def create_back_markup(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back_button = types.KeyboardButton("🔙 Вернуться в главное меню")
        markup.add(back_button)
        return markup
