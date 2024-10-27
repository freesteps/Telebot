# handlers/agreement.py
from telebot import types
from handlers.base import BaseHandler
from utils.storage import *
from utils.logger import log_user_action, logger  # Импортируем logger

class AgreementHandler(BaseHandler):
    def __init__(self, bot, test_handler):
        super().__init__(bot)
        self.test_handler = test_handler  # Ссылка на TestHandler

    def send_agreement(self, message):
        user_id = message.chat.id
        username = message.from_user.username

        # Чтение пользовательского соглашения из файла
        try:
            with open("user_agreement.txt", "r", encoding="utf-8") as f:
                agreement_text = f.read()
        except FileNotFoundError:
            self.bot.send_message(
                user_id,
                text="⚠️ Не удалось найти файл с пользовательским соглашением. Пожалуйста, свяжитесь с администратором."
            )
            log_user_action(user_id, username, "Ошибка: user_agreement.txt не найден")
            logger.error(f"user_agreement.txt не найден для пользователя ID: {user_id}, username: {username}")
            return

        # Создание кнопки "принять условия"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        accept_button = types.KeyboardButton("✅ Принять условия")
        markup.add(accept_button)

        self.bot.send_message(
            user_id,
            text=f"{agreement_text}\n\nПожалуйста, примите условия соглашения, нажав кнопку ниже.",
            reply_markup=markup
        )
        log_user_action(user_id, username, "Отправлено пользовательское соглашение")
        logger.info(f"Отправлено пользовательское соглашение пользователю ID: {user_id}, username: {username}")
        set_state(user_id, STATE_AGREEMENT)

    def handle_accept_agreement(self, message):
        user_id = message.chat.id
        username = message.from_user.username
        action = message.text

        if action == "✅ Принять условия":
            self.bot.send_message(
                user_id,
                text="Спасибо за принятие условий. Начнем тестирование.",
                reply_markup=self.create_remove_markup()
            )
            log_user_action(user_id, username, "Принял условия соглашения")
            logger.info(f"Пользователь ID: {user_id}, username: {username} принял условия соглашения")
            set_state(user_id, STATE_TEST_QUESTION_1)
            # Отправляем первый вопрос теста
            self.test_handler.send_question_1(message)
        else:
            self.bot.send_message(
                user_id,
                text="Пожалуйста, примите условия соглашения, нажав соответствующую кнопку.",
                reply_markup=self.create_agreement_markup()
            )
            log_user_action(user_id, username, "Попытка не принять условия соглашения")
            logger.warning(f"Пользователь ID: {user_id}, username: {username} попытался не принять условия соглашения")

    def create_remove_markup(self):
        return types.ReplyKeyboardRemove()

    def create_agreement_markup(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        accept_button = types.KeyboardButton("✅ Принять условия")
        markup.add(accept_button)
        return markup
