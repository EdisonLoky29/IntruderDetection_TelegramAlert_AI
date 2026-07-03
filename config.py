import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
CHAT_ID = os.getenv("CHAT_ID", "")

CAMERA_INDEX = int(os.getenv("CAMERA_INDEX", "0"))
MODEL_PATH = os.getenv("MODEL_PATH", "yolov8n.pt")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", "0.5"))
ALERT_COOLDOWN_SECONDS = float(os.getenv("ALERT_COOLDOWN_SECONDS", "10"))
ALARM_SOUND_PATH = os.getenv("ALARM_SOUND_PATH", "assets/alarm.wav")

ROI_WIDTH_FRACTION = float(os.getenv("ROI_WIDTH_FRACTION", "0.4"))
ROI_HEIGHT_FRACTION = float(os.getenv("ROI_HEIGHT_FRACTION", "0.4"))
