import json
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

with open(r"D:\Paython_4_darslik\pythonProject2\Teligram_bot\config.json", "r") as file:
    config = json.load(file)
TOKEN = config["TELEGRAM_BOT_TOKEN"]

ASK_NAME, ASK_SURNAME, ASK_PHONE = range(3)

async def welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_text(
        "Что умеет этот бот?\n\n"
        "Assolomu Aleykum!\n\n"
        "Men siz izlagan musiqangizni topishga yordam beraman 🎧\n\n"
        "Siz izlayotgan qo'shiqni topishim uchun quyidagilardan birini yuboring:\n"
        "• Qo'shiq nomi yoki ijrochi ismi\n"
        "• Video\n"
        "• Qo'shiq matni\n"
        "• Ovozli xabar\n"
        "• Video xabar\n"
        "• Tik Tokdagi video xovalasi\n"
        "• Instagramdagi video xovalasi"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Assalomu alaykum! Botdan foydalanishni boshlash uchun iltimos, ismingizni kiriting:")
    return ASK_NAME

async def ask_surname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Rahmat! Endi familiyangizni kiriting:")
    return ASK_SURNAME

async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["surname"] = update.message.text
    keyboard = [
        [KeyboardButton("📱 Telefon raqamni yuborish", request_contact=True)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Endi telefon raqamingizni yuboring:", reply_markup=reply_markup)
    return ASK_PHONE

async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    contact = update.message.contact
    if contact:
        context.user_data["phone"] = contact.phone_number
        
        user_data = {
            "name": context.user_data["name"],
            "surname": context.user_data["surname"],
            "phone": context.user_data["phone"]
        }
        with open("user_data.json", "a") as file:
            file.write(json.dumps(user_data) + "\n")

        await update.message.reply_text(
            "Rahmat! Endi botdan foydalanishingiz mumkin 🎧"
        )
        return ConversationHandler.END
    else:
        await update.message.reply_text("Iltimos, telefon raqamingizni yuboring.")
        return ASK_PHONE

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_message))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_surname)],
            ASK_SURNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
            ASK_PHONE: [MessageHandler(filters.CONTACT, handle_phone)]
        },
        fallbacks=[CommandHandler("start", start)]
    )

    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()

if __name__ == '__main__':
    main()
