# Telegram Trends Bot (Webhook + Flask)

## Описание
Этот бот автоматически отслеживает тренды по ключевым словам в Google Trends и присылает их в Telegram при команде `/check`.

## Как развернуть
1. Залей проект в GitHub
2. Создай новый веб-сервис на https://render.com
3. Укажи:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
4. Установи переменные окружения:
   - `TELEGRAM_TOKEN`: токен бота
   - `APP_URL`: адрес сервиса (например, `https://your-app-name.onrender.com`)
