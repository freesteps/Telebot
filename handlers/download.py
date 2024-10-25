# handlers/download.py
from telebot import types
from handlers.base import BaseHandler
from utils.storage import set_state, STATE_DOWNLOAD_APP, STATE_MAIN_MENU
from utils.logger import log_user_action
from handlers.menu import MenuHandler

class DownloadHandler(BaseHandler):
    def handle_download_app(self, message):
        user_id = message.chat.id
        username = message.from_user.username
        action = message.text

        if action == "📲 iOS":
            self.bot.send_message(
                user_id,
                text="Ссылка для загрузки Poizon на iOS: https://apps.apple.com/ru/app/..."
            )
            platform = "iOS"
        elif action == "📲 Android":
            self.bot.send_message(
                user_id,
                text="Ссылка для загрузки Poizon на Android: https://m.anxinapk.com/rj/12201303.html"
            )
            platform = "Android"
        else:
            self.bot.send_message(
                user_id,
                text="Пожалуйста, выберите платформу для загрузки.",
                reply_markup=self.create_platform_markup()
            )
            return  # Выход из функции, чтобы не менять статус на главное меню, если платформа не выбрана

        log_user_action(user_id, username, f"Скачал Poizon на {platform}")

        # После отправки ссылки, устанавливаем состояние главного меню
        set_state(user_id, STATE_MAIN_MENU)
        menu_handler = MenuHandler(self.bot)
        menu_handler.main_menu(message)

    def create_platform_markup(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        ios_button = types.KeyboardButton("📲 iOS")
        android_button = types.KeyboardButton("📲 Android")
        back_button = types.KeyboardButton("🔙 Вернуться в главное меню")
        markup.add(ios_button, android_button, back_button)
        return markup
