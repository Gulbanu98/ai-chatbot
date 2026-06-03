print ("Bot started")
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import json
from config import BOT_TOKEN, ADMIN_ID

# загрузка/сохранение данных
def load_data():
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"users": {}}

def save_data(data):
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_data()

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if user_id not in data["users"]:
        data["users"][user_id] = {
            "step": "choose_project",
            "answers": []
        }
        save_data(data)

    keyboard = [["X5", "Энергетик"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Привет! Выбери проект:",
        reply_markup=markup
    )

# обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text

    if user_id not in data["users"]:
        await update.message.reply_text("Напиши /start")
        return

    user = data["users"][user_id]

    # выбор проекта
    if user["step"] == "choose_project":
        if text in ["X5", "Энергетик"]:
            user["project"] = text
            user["step"] = "question_1"
            user["answers"] = []
            save_data(data)

            await update.message.reply_text("Вопрос 1: Представься, пожалуйста.")
        else:
            await update.message.reply_text("Выбери кнопку: X5 или Энергетик")
        return

    # сбор ответов
    if user["step"].startswith("question"):
        user["answers"].append(text)

        q_num = len(user["answers"]) + 1

        if q_num > 3:
            user["step"] = "done"
            save_data(data)

            await update.message.reply_text("Спасибо! Ответы записаны.")
            return

        save_data(data)
        await update.message.reply_text(f"Вопрос {q_num}: напиши ответ.")

# запуск бота
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if name == "__main__":
    main()
