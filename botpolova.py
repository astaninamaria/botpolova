from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import logging

# Ваш токен и ID администратора
TOKEN = "7832591309:AAFpuUy02eBoH717LuB-7OO72CM2iROm_w4"
ADMIN_ID = 673377646  # Вставьте сюда ID администратора

# Настройка логирования
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Кнопки для информации
route_button = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text="Посмотреть маршрут", url="https://yandex.ru/maps/-/CHBL6P-3")]]
)

doctor_info = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text="Подробнее", url="https://drevgeniyapolova.tilda.ws/")]]
)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветствие"""
    logger.info(f"User {update.effective_user.id} started the bot.")
    await update.message.reply_text(
        "Здравствуйте! Чтобы написать мне или найти нужную информацию, выберите команду в левом меню."
    )

# Обработка "Записаться на прием"
async def request_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запрос описания проблемы"""
    await update.message.reply_text(
        "Объясните, какая проблема вас беспокоит, и я вам отвечу. "
        "Выберем с вами удобное время."
    )
    logger.info(f"User {update.effective_user.id} requested an appointment.")

# Обработка "Адрес клиники"
async def address_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка адреса"""
    address_text = (
        "Я работаю по адресу: Заставская ул., 46, корп. 1, Санкт-Петербург\n"
        "[Открыть в Яндекс.Картах](https://yandex.ru/maps/-/CHBL6P-3)"
    )
    await update.message.reply_text(address_text, parse_mode="Markdown", reply_markup=route_button)
    logger.info(f"User {update.effective_user.id} asked for the clinic address.")

# Обработка "О враче и услугах"
async def doctor_info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправка информации о враче"""
    await update.message.reply_text("Подробнее о враче и услугах:", reply_markup=doctor_info)
    logger.info(f"User {update.effective_user.id} asked for doctor information.")

# Пересылка сообщения админу
async def forward_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Пересылка заявки админу"""
    user = update.effective_user
    message_text = update.message.text

    logger.info(f"Forwarding request from {user.full_name} (@{user.username}) to admin.")

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Новая заявка от {user.full_name} (@{user.username}):\n{message_text}"
    )
    await update.message.reply_text("Ваше сообщение принято. Отвечу вам в личном чате в ближайшее время.")

# Обработка команд из BotFather
async def command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команд из BotFather"""
    command_map = {
        "command1": request_handler,
        "command2": address_handler,
        "command3": doctor_info_handler
    }
    command = update.message.text.lstrip("/")
    if command in command_map:
        await command_map[command](update, context)
    else:
        await forward_request(update, context)

# Основная функция
def main():
    """Запуск бота"""
    application = ApplicationBuilder().token(TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("command1", request_handler))
    application.add_handler(CommandHandler("command2", address_handler))
    application.add_handler(CommandHandler("command3", doctor_info_handler))

    # Пересылка сообщений админу (всё, что не является командой)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_request))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
