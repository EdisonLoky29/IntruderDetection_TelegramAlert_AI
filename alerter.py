from datetime import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import cv2
import requests

import config

TELEGRAM_API_BASE = "https://api.telegram.org/bot{token}/sendPhoto"


class TelegramAlerter:
    def __init__(self, token: str = None, chat_id: str = None):
        self.token = token or config.TELEGRAM_TOKEN
        self.chat_id = chat_id or config.CHAT_ID
        if not self.token or not self.chat_id:
            raise ValueError(
                "TELEGRAM_TOKEN and CHAT_ID must be set in the .env file."
            )

    def send_intrusion_alert(self, frame) -> bool:
        """Encodes the frame as JPEG and sends it to Telegram with a caption."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        caption = f"INTRUSO DETECTADO - {timestamp}"

        success, encoded_image = cv2.imencode(".jpg", frame)
        if not success:
            return False

        url = TELEGRAM_API_BASE.format(token=self.token)
        files = {"photo": ("intrusion.jpg", encoded_image.tobytes(), "image/jpeg")}
        data = {"chat_id": self.chat_id, "caption": caption}

        try:
            response = requests.post(url, files=files, data=data, timeout=10, verify=False)
            if response.status_code != 200:
                print(f"[{timestamp}] RECHAZO DE TELEGRAM: {response.text}")
                return False
            return True
        except Exception as exc:
            print(f"[{timestamp}] Failed to send Telegram alert: {exc}")
            return False
