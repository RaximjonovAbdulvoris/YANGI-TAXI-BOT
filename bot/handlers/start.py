from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters

MENU_DRIVER = "📝 Ulanish uchun Ariza"
MENU_CONTACT = "Bog'lanish uchun"

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [[MENU_DRIVER], [MENU_CONTACT]],
    resize_keyboard=True,
)

WELCOME_TEXT = (
    "🚖 *YANGI TAXI’ga xush kelibsiz!*\n\n"
    "Kerakli bo‘limni tanlang:\n\n"
    "📝 *Ulanish uchun ariza* — YANGI TAXI haydovchisi bo‘lish uchun ariza yuboring.\n\n"
    "📞 *Aloqa* — Biz bilan bog‘lanish uchun aloqa ma’lumotlarini oling.\n\n"
    "👇 Davom etish uchun quyidagi tugmalardan birini tanlang."
)

CONTACT_TEXT = (
    "📞 Aloqa: +998 33 113-80-85 | +998 33 920-44-44\n"
    "✈️ Telegram: @arizalarnamangan"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text(
        WELCOME_TEXT,
        parse_mode="Markdown",
        reply_markup=MAIN_KEYBOARD,
    )
    return ConversationHandler.END


async def show_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        CONTACT_TEXT,
        reply_markup=MAIN_KEYBOARD,
        disable_web_page_preview=True,
    )


def build_contact_handler() -> MessageHandler:
    return MessageHandler(filters.Regex(f"^{MENU_CONTACT}$"), show_contact)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text(
        "❌ Bekor qilindi. Qaytadan boshlash uchun /start bosing.",
        reply_markup=MAIN_KEYBOARD,
    )
    return ConversationHandler.END
