# main.py
import telebot
import config
from utils.logger import logger, log_user_action
from utils.storage import (
    set_state,
    get_state,
    save_user_source,
    STATE_MAIN_MENU,
    STATE_ORDER,
    STATE_ORDER_DETAILS,
    STATE_TRACK_ORDER,
    STATE_FEEDBACK,
    STATE_CALCULATE_COST,
    STATE_MAIN_INFO,
    STATE_DOWNLOAD_APP,
    STATE_AGREEMENT,
    STATE_TEST_QUESTION_1,
    STATE_TEST_QUESTION_2
)
from handlers import (
    MenuHandler,
    OrderHandler,
    FeedbackHandler,
    CalculateHandler,
    DownloadHandler,
    MainInfoHandler,
    AgreementHandler,
    TestHandler
)

# Настройка логирования
logger.info("Запуск бота...")

# Инициализация бота
bot = telebot.TeleBot(config.TOKEN)

# Инициализация обработчиков
menu_handler = MenuHandler(bot)
order_handler = OrderHandler(bot)
feedback_handler = FeedbackHandler(bot)
calculate_handler = CalculateHandler(bot)
download_handler = DownloadHandler(bot)
main_info_handler = MainInfoHandler(bot)
test_handler = TestHandler(bot, menu_handler)  # Передача menu_handler
agreement_handler = AgreementHandler(bot, test_handler)  # Передача test_handler


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    username = message.from_user.username

    logger.info(f"Получен /start от пользователя ID: {user_id}, username: {username}")

    if not username:
        bot.send_message(
            user_id,
            text="⚠️ У вас отсутствует username в Telegram. Пожалуйста, установите его в настройках аккаунта и повторите попытку."
        )
        logger.warning(f"ID: {user_id}: Отсутствует username, взаимодействие не начато.")
        return

    # Получаем параметр из ссылки (если он передан)
    parts = message.text.split(' ')
    ref_source_code = parts[1] if len(parts) > 1 else None
    ref_source = config.REF_SOURCES.get(ref_source_code, "Неизвестный источник")  # По умолчанию "Неизвестный источник"

    # Проверяем, новый ли пользователь
    is_new_user = save_user_source(user_id, username, ref_source)

    if is_new_user:
        # Новый пользователь, отправляем соглашение
        agreement_handler.send_agreement(message)
        return

    # Логируем действие
    log_user_action(user_id, username, "старт")

    # Отправляем приветственное сообщение
    bot.send_message(user_id, text=f"Добро пожаловать!\n{config.WORK_SCHEDULE}")
    menu_handler.main_menu(message)


@bot.message_handler(content_types=['text', 'photo'])
def handle_messages(message):
    user_id = message.chat.id
    username = message.from_user.username

    logger.info(
        f"Получено сообщение от пользователя ID: {user_id}, username: {username}, content_type: {message.content_type}")

    if not username:
        bot.send_message(
            user_id,
            text="⚠️ У вас отсутствует username в Telegram. Пожалуйста, установите его в настройках аккаунта и повторите попытку."
        )
        logger.warning(f"ID: {user_id}: Отсутствует username, действие не выполнено.")
        return

    # Обновляем информацию о пользователе
    save_user_source(user_id, username, "Неизвестный источник")  # Можно улучшить, чтобы сохранять актуальный источник

    # Логируем действие
    action = message.text if message.content_type == 'text' else 'Фото'
    log_user_action(user_id, username, action)

    # Получаем текущее состояние пользователя
    state = get_state(user_id, STATE_MAIN_MENU)

    if state == STATE_AGREEMENT:
        agreement_handler.handle_accept_agreement(message)
    elif state == STATE_TEST_QUESTION_1:
        test_handler.handle_question_1(message)
    elif state == STATE_TEST_QUESTION_2:
        test_handler.handle_question_2(message)
    elif message.text == "🔙 Вернуться в главное меню":
        menu_handler.main_menu(message)
    elif state == STATE_MAIN_MENU:
        handle_main_menu_actions(message)
    elif state == STATE_ORDER:
        order_handler.handle_order_photo(message)
    elif state == STATE_ORDER_DETAILS:
        order_handler.handle_order_details(message)
    elif state == STATE_TRACK_ORDER:
        track_order(message)
    elif state == STATE_FEEDBACK:
        feedback_handler.handle_feedback(message)
    elif state == STATE_CALCULATE_COST:
        calculate_handler.handle_calculate_cost(message)
    elif state == STATE_MAIN_INFO:
        main_info_handler.handle_main_info(message)
    elif state == STATE_DOWNLOAD_APP:
        download_handler.handle_download_app(message)
    else:
        logger.warning(f"ID: {user_id} (@{username}): Нераспознанная команда.")
        bot.send_message(message.chat.id, text="На такую команду я не запрограммирован.")


def handle_main_menu_actions(message):
    user_id = message.chat.id
    username = message.from_user.username
    action = message.text

    log_user_action(user_id, username, action)

    if action == "🛒 Сделать заказ":
        bot.send_message(
            user_id,
            text="Пожалуйста, отправьте фото товара с Poizon, который хотите заказать.\n❗❗❗ВАЖНО❗❗❗\nДоставка осуществляется только на территорию РФ.",
            reply_markup=order_handler.create_back_markup()
        )
        set_state(user_id, STATE_ORDER)
    elif action == "📦 Отследить заказ":
        bot.send_message(
            user_id,
            text="Вы выбрали 'Отследить заказ'.\nЗаказ можно отследить на сайте: https://www.cdek.ru/ru/cabinet/orders",
            reply_markup=order_handler.create_back_markup()
        )
        set_state(user_id, STATE_TRACK_ORDER)
    elif action == "💬 Отзывы и предложения":
        bot.send_message(
            user_id,
            text="Вы выбрали 'Отзывы и предложения'. Пожалуйста, оставьте ваш отзыв или предложение.",
            reply_markup=feedback_handler.create_back_markup()
        )
        set_state(user_id, STATE_FEEDBACK)
    elif action == "📈 Рассчитать стоимость":
        bot.send_message(
            user_id,
            text="Введите стоимость в юанях. Минимум 100 CNY.",
            reply_markup=calculate_handler.create_back_markup()
        )
        set_state(user_id, STATE_CALCULATE_COST)
    elif action == "ℹ️ Основная информация":
        bot.send_message(
            user_id,
            text=f"{main_info_handler.get_main_info_text()}\n\n{config.WORK_SCHEDULE}",
            reply_markup=main_info_handler.create_info_markup()
        )
        set_state(user_id, STATE_MAIN_INFO)
    elif action == "📄 Как происходит выкуп":
        bot.send_message(
            user_id,
            text=main_info_handler.get_purchase_info_text(),
            reply_markup=order_handler.create_back_markup()
        )
        set_state(user_id, STATE_MAIN_MENU)
    elif action == "📲 Скачать Poizon":
        bot.send_message(
            user_id,
            text="Выберите вашу платформу:",
            reply_markup=download_handler.create_platform_markup()
        )
        set_state(user_id, STATE_DOWNLOAD_APP)
    else:
        logger.warning(f"ID: {user_id} (@{username}): Нераспознанное действие в главном меню.")
        bot.send_message(user_id, "Пожалуйста, выберите одну из предложенных опций.",
                         reply_markup=order_handler.create_back_markup())


def track_order(message):
    user_id = message.chat.id
    username = message.from_user.username

    bot.send_message(
        user_id,
        text="Вы можете отследить свой заказ по следующей ссылке: https://www.cdek.ru/ru/cabinet/orders",
        reply_markup=order_handler.create_back_markup()
    )
    log_user_action(user_id, username, "Отследить заказ")
    set_state(user_id, STATE_MAIN_MENU)


if __name__ == "__main__":
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(f"Ошибка в процессе работы бота: {e}")
