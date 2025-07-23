from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)
from flask import Flask
import threading
import random
import asyncio

# 🔧 Конфигурация
TOKEN = "7436013012:AAG-zReSmx4agXxrjUPpYXF_hCFA_JlsPOw"
MASTER_CHAT_ID = 5225197085

# 📜 Цитаты от чайного пьяницы
tea_quotes = [
    "🍵 Иногда чашка чая говорит больше, чем тысяча слов.",
    "🍃 Тишина между глотками — тоже часть церемонии.",
    "🐉 Там, где чай — там дом.",
    "☁️ Завари чай, пусть он заварит и тебя.",
    "🫖 Горячая вода не делает чай сильным, она раскрывает его суть.",
    "🌿 Пей чай, пока мир сам не остынет.",
    "🍵 Даже самый мутный пуэр находит свою прозрачность.",
    "🐢 Мудрость — это умение не спешить даже с чаем.",
    "⛩️ В чайной чаше — отражение неба.",
    "🔥 Пусть вода закипит, а мысли остынут.",
    "🪷 Там где есть чай, нет спешки.",
    "🌫️ Первый глоток — для тела. Второй — для духа. Третий — для пустоты.",
    "🌌 Кто спешит с чаем — опаздывает к себе.",
    "🌕 Настоящий чайный пьяница пьёт, чтобы пробудиться, а не забыться.",
    "🍂 Пей чай и позволяй жизни происходить.",
    "📿 Чай — мой монах, а я его послушник.",
    "🪵 Тот, кто разделил с тобой чай — больше, чем гость.",
    "💨 Чай не требует слов, только присутствия.",
    "🌬️ Даже самый крепкий чай не заменит крепости внутри.",
    "🎋 Пусть чай вымоет суету из сердца.",
    # добавь ещё если хочешь — всего 100
]

# 🧠 Состояния
NAME, DATE, PLACE, COMMENTS, PHONE, NOTE, REMIND = range(7)

# 🌐 Flask для Render
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is alive"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# 📍 Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != MASTER_CHAT_ID:
        await context.bot.send_message(MASTER_CHAT_ID, f"👤 Новый пользователь: @{update.effective_user.username or 'без ника'}")
    keyboard = [
        ["🧘 О практике", "📅 Записаться"],
        ["🍵 Цитата дня от чайного пьяницы", "🤝 Поддержать проект"],
        ["💌 Оставить записку"]
    ]
    await update.message.reply_text(
        "🛠️ Добро пожаловать в пространство *«Гвозди и Листья»* 🍃\n\n"
        "🔩 Стояние на гвоздях\n"
        "🍵 Чайные церемонии\n"
        "💆 Банки\n"
        "💬 Душевные разговоры\n"
        "🏕 Выездные практики на природе\n\n"
        "👇 Выбери действие:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode="Markdown"
    )

# 📅 Запись
async def sign_up(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Как тебя зовут?")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['name'] = update.message.text
    await update.message.reply_text("Когда удобно? (дата/время)")
    return DATE

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['date'] = update.message.text
    await update.message.reply_text("Где провести? (дома, в лесу, у меня?)")
    return PLACE

async def get_place(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['place'] = update.message.text
    await update.message.reply_text("Пожелания или мысли?")
    return COMMENTS

async def get_comments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['comments'] = update.message.text
    await update.message.reply_text("Оставь номер телефона 📱")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    user = update.message.from_user
    text = (
        f"📥 *Новая заявка:*\n"
        f"👤 Имя: {context.user_data['name']}\n"
        f"📅 Когда: {context.user_data['date']}\n"
        f"📍 Где: {context.user_data['place']}\n"
        f"💬 Мысли: {context.user_data['comments']}\n"
        f"📱 Телефон: {context.user_data['phone']}\n"
        f"Telegram: @{user.username or 'нет'}"
    )
    await context.bot.send_message(MASTER_CHAT_ID, text, parse_mode="Markdown")
    await update.message.reply_text("Спасибо! Я скоро с тобой свяжусь 🙌")
    return ConversationHandler.END

# 💌 Записка
async def note_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Оставь записку, и она будет передана лично 📬")
    return NOTE

async def receive_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    msg = f"📩 *Записка от @{user.username or 'аноним'}:*\n\n{update.message.text}"
    await context.bot.send_message(MASTER_CHAT_ID, msg, parse_mode="Markdown")
    await update.message.reply_text("Спасибо, записка доставлена 🙏")
    return ConversationHandler.END

# 🤝 Поддержка
async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💚 Хочешь поддержать проект?\n\n"
        "📲 Перевод по номеру: *+7 912 852‑81‑81*\n"
        "_Сбербанк / Т-Банк_ или приходи за чаем 🐉",
        parse_mode="Markdown"
    )

# 🍵 Цитата дня
async def tea_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quote = random.choice(tea_quotes)
    await update.message.reply_text(quote)

# 🧘 О практике
async def practice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌿 «Гвозди и Листья» — место, где возвращаются к себе:\n\n"
        "🔩 Гвозди — заземление, принятие\n"
        "🍵 Чай — тишина, вкус, внимание\n"
        "💬 Разговор — от сердца\n"
        "💆 Банки — мягкое прикосновение к телу\n"
        "🏕 Церемонии под небом и с природой"
    )

# 🌀 Неизвестное
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Не понял тебя 🙃 Нажми кнопку ниже")

# ▶️ MAIN
def main():
    threading.Thread(target=run_flask).start()
    app_ = ApplicationBuilder().token(TOKEN).build()

    app_.add_handler(CommandHandler("start", start))
    app_.add_handler(MessageHandler(filters.Regex("🧘 О практике"), practice))
    app_.add_handler(MessageHandler(filters.Regex("🤝 Поддержать проект"), support))
    app_.add_handler(MessageHandler(filters.Regex("🍵 Цитата дня от чайного пьяницы"), tea_quote))

    app_.add_handler(ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("📅 Записаться"), sign_up)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
            PLACE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_place)],
            COMMENTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_comments)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        },
        fallbacks=[]
    ))

    app_.add_handler(ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("💌 Оставить записку"), note_entry)],
        states={NOTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_note)]},
        fallbacks=[]
    ))

    app_.add_handler(MessageHandler(filters.COMMAND, unknown))
    app_.add_handler(MessageHandler(filters.TEXT, unknown))

    app_.run_polling()

if __name__ == "__main__":
    main()
