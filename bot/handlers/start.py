from pathlib import Path

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters

MENU_DRIVER = "📝 Ulanish uchun Ariza"
MENU_CONTACT = "📞 Bog'lanish uchun"
MENU_OFFICE = "📍 Ofis manzili"
OFFICE_PHOTO = Path(__file__).resolve().parents[1] / "templates" / "office.png"
OFFICE_CAPTION = (
    "📍 <b>YANGI TAXI ofisi</b>\n\n"
    "Mo‘ljal: Zarkan kordiyalogiya\n"
    "Va Byd namangan yonida\n\n"
    "👇 Manzilni ko‘rish uchun «Xaritada ochish» tugmasini bosing."
)
OFFICE_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("📍 Xaritada ochish", url="https://yandex.ru/maps/-/CTtEuSZe")],
])

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [[MENU_DRIVER], [MENU_CONTACT], [MENU_OFFICE]],
    resize_keyboard=True,
)

WELCOME_TEXT = (
    "🚖 *YANGI TAXI’ga xush kelibsiz!*\n\n"
    "Kerakli bo‘limni tanlang:\n\n"
    "📝 *Ulanish uchun ariza* — YANGI TAXI haydovchisi bo‘lish uchun ariza yuboring.\n\n"
    "📞 *Aloqa* — Biz bilan bog‘lanish uchun aloqa ma’lumotlarini oling.\n\n"
    "📍 *Ofis manzili* — Ofis rasmi, mo‘ljal va xaritani ko‘ring.\n\n"
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
    return MessageHandler(filters.Regex(r"^(?:📞 )?Bog'lanish uchun$"), show_contact)


async def show_office(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    cached_photo = context.bot_data.get("office_photo_file_id")
    if cached_photo:
        await update.message.reply_photo(
            photo=cached_photo, caption=OFFICE_CAPTION,
            parse_mode="HTML", reply_markup=OFFICE_KEYBOARD,
        )
    else:
        with OFFICE_PHOTO.open("rb") as photo:
            sent = await update.message.reply_photo(
                photo=photo, caption=OFFICE_CAPTION,
                parse_mode="HTML", reply_markup=OFFICE_KEYBOARD,
            )
        if sent.photo:
            context.bot_data["office_photo_file_id"] = sent.photo[-1].file_id


def build_office_handler() -> MessageHandler:
    return MessageHandler(filters.Regex(f"^{MENU_OFFICE}$"), show_office)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text(
        "❌ Bekor qilindi. Qaytadan boshlash uchun /start bosing.",
        reply_markup=MAIN_KEYBOARD,
    )
    return ConversationHandler.END
