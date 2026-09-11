from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters

MENU_DRIVER = "📝 Ulanish uchun Ariza"
MENU_BRAND = "🎨 Brend Ariza"
MENU_PAYOUT = "💰 PUL YECHISH BOTI"
MENU_CONTACT = "Bog'lanish uchun"

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [[MENU_DRIVER], [MENU_CONTACT]],
    resize_keyboard=True,
)

WELCOME_TEXT = (
    "🚖 *WB TAXI LEGENDA* botiga xush kelibsiz!\n\n"
    "Quyidagi menyulardan birini tanlang:\n\n"
    "📝 *Ulanish uchun Ariza* — Haydovchilik uchun ariza\n"
    "*Bog'lanish uchun* — Aloqa ma'lumotlari"
)

CONTACT_TEXT = (
    "📞 Aloqa: +998 33 113-80-85 | +998 33 920-44-44\n"
    "✈️ Telegram: @arizalarnamangan"
)

PAYOUT_TEXT = (
    "💰 *PUL YECHISH BOTI:* @legendapulbot\n\n"
    "📞 *PARK NOMERI:* +998781505050\n\n"
    "✉️ *TELEGRAM ORQALI MUROJAT:* @WBLEGENDATAXI"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text(
        WELCOME_TEXT,
        parse_mode="Markdown",
        reply_markup=MAIN_KEYBOARD,
    )
    return ConversationHandler.END


async def show_payout(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        PAYOUT_TEXT,
        parse_mode="Markdown",
        reply_markup=MAIN_KEYBOARD,
        disable_web_page_preview=True,
    )


async def show_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        CONTACT_TEXT,
        reply_markup=MAIN_KEYBOARD,
        disable_web_page_preview=True,
    )


def build_contact_handler() -> MessageHandler:
    return MessageHandler(filters.Regex(f"^{MENU_CONTACT}$"), show_contact)


def build_payout_handler() -> MessageHandler:
    return MessageHandler(filters.Regex(f"^{MENU_PAYOUT}$"), show_payout)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text(
        "❌ Bekor qilindi. Qaytadan boshlash uchun /start bosing.",
        reply_markup=MAIN_KEYBOARD,
    )
    return ConversationHandler.END
