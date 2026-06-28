# Intruder Detection & Alert System

Real-time webcam surveillance system that detects people entering a restricted
zone (ROI) using YOLOv8, then triggers a local alarm sound and a Telegram
alert with a snapshot of the intrusion.

Runs entirely on CPU — no GPU/CUDA required.

## Project structure

```
security-system/
├── main.py          # entry point, video loop
├── detector.py       # YOLOv8 person detection logic
├── alerter.py         # Telegram alert sender
├── zone.py            # ROI definition and containment check
├── alarm.py            # sound playback (pygame)
├── config.py            # loads .env variables
├── .env.example          # template with TELEGRAM_TOKEN and CHAT_ID
├── requirements.txt
└── assets/alarm.wav        # alarm sound (add your own .wav file)
```

## Setup

### 1. Install dependencies

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

The first run will auto-download `yolov8n.pt` (~6 MB) via `ultralytics`.

### 2. Configure environment variables

Copy the template and fill in your values:

```bash
copy .env.example .env
```

Edit `.env`:

```
TELEGRAM_TOKEN=your_bot_token_here
CHAT_ID=your_chat_id_here
```

### 3. Get a Telegram bot token and chat ID

1. Open Telegram and search for **@BotFather**.
2. Send `/newbot`, follow the prompts, and copy the **token** it gives you
   (looks like `123456789:ABCdefGhIJKlmNoPQRstuVWXyz`).
3. Start a chat with your new bot (search for its username and press
   **Start**), or add it to a group.
4. Get your chat ID:
   - Send any message to the bot.
   - Visit `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` in a browser.
   - Look for `"chat":{"id":123456789, ...}` in the JSON response — that
     number is your `CHAT_ID`.
5. Paste both values into `.env`.

### 4. Add an alarm sound

Place a `.wav` file at `assets/alarm.wav` (or change `ALARM_SOUND_PATH` in
`.env`). If no file is found, the alarm runs silently and a warning is
logged — detection and Telegram alerts still work.

## Running

```bash
python main.py
```

- A window shows the live feed with bounding boxes around detected people,
  the restricted zone overlay (green = clear, red = intrusion), and a status
  label.
- Press **q** to quit.
- Alerts (alarm + Telegram) are rate-limited by `ALERT_COOLDOWN_SECONDS`
  (default 10s) to avoid spam while someone lingers in the zone.

## Adjusting the restricted zone

The ROI is a rectangle centered on the frame, sized as a fraction of frame
width/height. Edit these in `.env`:

```
ROI_WIDTH_FRACTION=0.4
ROI_HEIGHT_FRACTION=0.4
```

For a custom polygon shape instead of a centered rectangle, edit
`get_center_rectangle_roi` in `zone.py`.

## Packaging as a standalone executable (PyInstaller)

```bash
pip install pyinstaller
pyinstaller --name IntruderDetection ^
  --add-data "assets;assets" ^
  --collect-all ultralytics ^
  --onefile main.py
```

Notes:
- Ship `yolov8n.pt` and `.env` alongside the generated executable in
  `dist/` (or bundle the model with `--add-data "yolov8n.pt;."`).
- `--onefile` increases startup time due to extraction; use `--onedir` for
  faster repeated launches during a demo.
- Test the executable from a clean folder to confirm all data files
  (`.env`, `assets/`, model weights) resolve correctly relative to the exe.

## Troubleshooting

- **Camera doesn't open**: try a different `CAMERA_INDEX` (0, 1, 2...) in
  `.env`.
- **No Telegram alerts**: check the console log for the HTTP error; verify
  the bot token and that you've sent at least one message to the bot before
  fetching `CHAT_ID`.
- **Slow detection**: YOLOv8n is the smallest model and should run in
  near-real-time on most CPUs; lower `CONFIDENCE_THRESHOLD` only if you're
  missing detections, not for performance.
