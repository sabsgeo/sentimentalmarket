from .base import INotify
import requests

import logging

logger = logging.getLogger(__name__)

class TelegramNotify(INotify):
    
    def send_notification(self, bot_key, channel_id, message) -> None :
        send_message_url = f'https://api.telegram.org/bot{bot_key}/sendMessage?chat_id={channel_id}&text={message}&parse_mode=markdown'
        req = requests.post(send_message_url)
        if req.status_code == 200:
            logger.info('Notification send')
        else:
            logger.error("Error in sending notifiction")
        