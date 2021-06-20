from .telegram import TelegramNotify
import threading


def notify(user_config, message):
    notification_mediums = user_config.notify_on
    if 'telegram' in notification_mediums:
        telegram_settings = user_config.telegram_settings
        channel_id = telegram_settings.channel_id
        bot_key = telegram_settings.bot_key
        threading.Thread(target=TelegramNotify().send_notification,
                         args=(bot_key, channel_id, message)).start()
