# handlers/test.py
from telebot import types
from handlers.base import BaseHandler
from utils.storage import set_state, STATE_TEST_QUESTION_2, STATE_MAIN_MENU, STATE_TEST_QUESTION_1
from utils.logger import log_user_action, logger  # Импортируем logger

class TestHandler(BaseHandler):
    def __init__(self, bot, menu_handler):
        super().__init__(bot)
        self.menu_handler = menu_handler  # Ссылка на MenuHandler

    def send_question_1(self, message):
        user_id = message.chat.id
        username = message.from_user.username

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_ya = types.KeyboardButton("я")
        button_buyer = types.KeyboardButton("байер")
        markup.add(button_ya, button_buyer)

        self.bot.send_message(
            user_id,
            text="1) Кто несет ответственность за товар, который не подошел по размеру?",
            reply_markup=markup
        )
        log_user_action(user_id, username, "Задано вопрос 1 теста")
        set_state(user_id, STATE_TEST_QUESTION_1)
        logger.info(f"Отправлен вопрос 1 теста пользователю ID: {user_id}, username: {username}")

    def handle_question_1(self, message):
        user_id = message.chat.id
        username = message.from_user.username
        answer = message.text.lower()

        if answer == "я":
            self.bot.send_message(
                user_id,
                text="Правильно! Перейдем к следующему вопросу.",
                reply_markup=self.create_remove_markup()
            )
            log_user_action(user_id, username, "Ответил на вопрос 1 правильно")
            set_state(user_id, STATE_TEST_QUESTION_2)
            self.send_question_2(message)
        elif answer == "байер":
            self.bot.send_message(
                user_id,
                text="Неправильно. Попробуйте еще раз.",
                reply_markup=self.create_retry_markup(["я", "байер"])
            )
            log_user_action(user_id, username, "Ответил на вопрос 1 неправильно")
            logger.info(f"Неправильный ответ на вопрос 1 от пользователя ID: {user_id}, username: {username}")
        else:
            self.bot.send_message(
                user_id,
                text="Пожалуйста, выберите один из предложенных вариантов.",
                reply_markup=self.create_retry_markup(["я", "байер"])
            )
            logger.info(f"Некорректный ответ на вопрос 1 от пользователя ID: {user_id}, username: {username}")

    def send_question_2(self, message):
        user_id = message.chat.id
        username = message.from_user.username

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_da = types.KeyboardButton("да")
        button_net = types.KeyboardButton("нет")
        markup.add(button_da, button_net)

        self.bot.send_message(
            user_id,
            text="2) Можно ли сделать возврат в случае брака?",
            reply_markup=markup
        )
        log_user_action(user_id, username, "Задано вопрос 2 теста")
        set_state(user_id, STATE_TEST_QUESTION_2)
        logger.info(f"Отправлен вопрос 2 теста пользователю ID: {user_id}, username: {username}")

    def handle_question_2(self, message):
        user_id = message.chat.id
        username = message.from_user.username
        answer = message.text.lower()

        if answer == "нет":
            self.bot.send_message(
                user_id,
                text="Правильно! Вы прошли тестирование. Добро пожаловать в главное меню.",
                reply_markup=self.create_remove_markup()
            )
            log_user_action(user_id, username, "Ответил на вопрос 2 правильно")
            set_state(user_id, STATE_MAIN_MENU)
            # Вызов главного меню
            self.menu_handler.main_menu(message)
            logger.info(f"Главное меню отправлено пользователю ID: {user_id}, username: {username}")
        elif answer == "да":
            self.bot.send_message(
                user_id,
                text="Неправильно. Попробуйте еще раз.",
                reply_markup=self.create_retry_markup(["да", "нет"])
            )
            log_user_action(user_id, username, "Ответил на вопрос 2 неправильно")
            logger.info(f"Неправильный ответ на вопрос 2 от пользователя ID: {user_id}, username: {username}")
        else:
            self.bot.send_message(
                user_id,
                text="Пожалуйста, выберите один из предложенных вариантов.",
                reply_markup=self.create_retry_markup(["да", "нет"])
            )
            logger.info(f"Некорректный ответ на вопрос 2 от пользователя ID: {user_id}, username: {username}")

    def create_remove_markup(self):
        return types.ReplyKeyboardRemove()

    def create_retry_markup(self, buttons):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*[types.KeyboardButton(btn) for btn in buttons])
        return markup
