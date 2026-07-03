# Sistema de Detección de Intrusos y Alertas

Sistema de vigilancia en tiempo real mediante webcam que detecta personas al
entrar en una zona restringida (ROI) utilizando YOLOv8. Cuando detecta una
intrusión, activa una alarma local y envía una alerta por Telegram con una
captura de la intrusión.

Funciona completamente en CPU, sin necesidad de GPU/CUDA.

## Estructura del proyecto

```text
security-system/
├── main.py          # punto de entrada, bucle principal de video
├── detector.py       # lógica de detección de personas con YOLOv8
├── alerter.py         # envío de alertas por Telegram
├── zone.py            # definición de la ROI y comprobación de contención
├── alarm.py            # reproducción del sonido (pygame)
├── config.py            # carga las variables de .env
├── .env.example          # plantilla con TELEGRAM_TOKEN y CHAT_ID
├── requirements.txt
└── assets/alarm.wav        # sonido de la alarma (agrega tu propio archivo .wav)
```

## Configuración

### 1. Instalar las dependencias

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

La primera ejecución descargará automáticamente `yolov8n.pt` (~6 MB) mediante `ultralytics`.

### 2. Configurar las variables de entorno

Copia la plantilla y completa tus valores:

```bash
copy .env.example .env
```

Edita `.env`:

```text
TELEGRAM_TOKEN=your_bot_token_here
CHAT_ID=your_chat_id_here
```

### 3. Obtener el token del bot de Telegram y el chat ID

1. Abre Telegram y busca **@BotFather**.
2. Envía `/newbot`, sigue las instrucciones y copia el **token** que te proporciona
   (tendrá un formato similar a `123456789:ABCdefGhIJKlmNoPQRstuVWXyz`).
3. Inicia un chat con tu nuevo bot (búscalo por su nombre de usuario y pulsa
   **Start**), o agrégalo a un grupo.
4. Obtén tu `CHAT_ID`:
   - Envía cualquier mensaje al bot.
   - Visita `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` desde un navegador.
   - Busca `"chat":{"id":123456789, ...}` en la respuesta JSON; ese número
     corresponde a tu `CHAT_ID`.
5. Pega ambos valores en `.env`.

### 4. Agregar un sonido de alarma

Coloca un archivo `.wav` en `assets/alarm.wav` (o cambia `ALARM_SOUND_PATH` en
`.env`). Si no se encuentra ningún archivo, la alarma se ejecutará en silencio
y se registrará una advertencia; la detección y las alertas de Telegram seguirán funcionando.

## Ejecución

```bash
python main.py
```

- Se abrirá una ventana con la transmisión en vivo, mostrando los cuadros delimitadores alrededor de las personas detectadas, la superposición de la zona restringida (verde = libre, rojo = intrusión) y una etiqueta de estado.
- Presiona **q** para salir.
- Las alertas (alarma + Telegram) están limitadas por `ALERT_COOLDOWN_SECONDS`
  (10 segundos por defecto) para evitar spam mientras una persona permanezca dentro de la zona.

## Ajustar la zona restringida

La ROI es un rectángulo centrado en el cuadro de video, cuyo tamaño se define
como una fracción del ancho y alto de la imagen. Modifica estos valores en `.env`:

```text
ROI_WIDTH_FRACTION=0.4
ROI_HEIGHT_FRACTION=0.4
```

Si deseas utilizar un polígono personalizado en lugar de un rectángulo centrado,
edita `get_center_rectangle_roi` en `zone.py`.

## Empaquetar como un ejecutable independiente (PyInstaller)

```bash
pip install pyinstaller
pyinstaller --name IntruderDetection ^
  --add-data "assets;assets" ^
  --collect-all ultralytics ^
  --onefile main.py
```

Notas:

- Coloca `yolov8n.pt` y `.env` junto al ejecutable generado dentro de `dist/`
  (o incluye el modelo con `--add-data "yolov8n.pt;."`).
- `--onefile` incrementa el tiempo de inicio debido a la extracción temporal de archivos; utiliza `--onedir` para obtener inicios más rápidos durante el desarrollo o demostraciones.
- Prueba el ejecutable desde una carpeta limpia para verificar que todos los archivos necesarios (`.env`, `assets/` y los pesos del modelo) se encuentren correctamente con respecto al ejecutable.

## Solución de problemas

- **La cámara no se abre**: prueba un valor diferente para `CAMERA_INDEX` (0, 1, 2...) en `.env`.
- **No se envían alertas por Telegram**: revisa el registro de la consola para identificar errores HTTP; verifica que el token del bot sea correcto y que hayas enviado al menos un mensaje al bot antes de obtener el `CHAT_ID`.
- **La detección es lenta**: YOLOv8n es el modelo más pequeño y debería ejecutarse casi en tiempo real en la mayoría de las CPU. Reduce `CONFIDENCE_THRESHOLD` únicamente si se están perdiendo detecciones, no como medida para mejorar el rendimiento.
