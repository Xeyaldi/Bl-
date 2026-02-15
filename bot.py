import logging
import os
import sys

# --- HEROKU PYTHON 3.13+ XƏTASI ÜÇÜN YAMAQ (BUNA TOXUNMA) ---
try:
    import imghdr
except ImportError:
    from types import ModuleType
    imghdr = ModuleType('imghdr')
    sys.modules['imghdr'] = imghdr
# ---------------------------------------------------------

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- AYARLAR ---
BOT_OWNER_ID = 8024893255 

BANNED_WORDS = [
    "bic", "gic", "peyser", "qodu", "ogras", "fahişe", "sherefsiz", "exlaqsiz", "gicbeser", "meymun", "andira", "zibil", "itoglu", "alcaq", "sherefsiz", "arsiz", "namussuz", "qancıq", "ogras", "tulku", "paxıl", "iyrenc", "mal", "eşşek", "it", "donuz", "heyvan", "qaltax", "qehbe", "bicinbalasi", "soxum", "var-yox", "nəsil", "itoglu", "itqizi", "gicbəsər", "kütbeyin", "şərəfsiz", "ləyaqətsiz", "mənliysiz", "namussuz", "abırsız", "həyasız", "üzsüz", "tərbiyəsiz", "mərifətsiz", "insafsız", "vicdansız", "itbalası", "donuzbalası", "yalançı", "fırıldaqçı", "oğru", "alçaq", "rəzil", "iyrənc", "murdar", "axmaq", "sarsaq", "ədəbsiz", "əxlaqsız", "pozğun", "nadan", "cahil", "qanmaz", "beyinsiz", "gicgah", "xiyar", "balqabaq", "qoyun", "keçi", "eşşək", "vəhşi", "itil", "rəddol"
]

settings = {"all_stickers_off": False}

# --- FUNKSİYALAR ---

async def is_creator(update: Update):
    if update.effective_chat.type == "private": return False
    member = await update.effective_chat.get_member(update.effective_user.id)
    return member.status == 'creator'

async def is_admin(update: Update):
    if update.effective_chat.type == "private": return True
    member = await update.effective_chat.get_member(update.effective_user.id)
    return member.status in ['administrator', 'creator']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = (
        f"👋 ꜱᴀʟᴀᴍ, {user.first_name}!\n\n"
        "🛡️ ᴍəɴ ǫʀᴜᴘʟᴀʀı ᴛəᴍɪᴢ ꜱᴀxʟᴀʏᴀɴ ᴘʀᴏꜰᴇꜱɪʏᴏɴᴀʟ ᴍᴏᴅᴇʀᴀᴛᴏʀ ʙᴏᴛᴀᴍ.\n"
        "✨ ǫʀᴜᴘʟᴀʀᴅᴀ ɴᴇǫᴀᴛɪᴠ ʜᴀʟʟᴀʀıɴ ǫᴀʀşıꜱıɴı ᴀʟıʀᴀᴍ."
    )
    keyboard = [
        [InlineKeyboardButton("📚 ᴋᴏᴍᴀɴᴅᴀʟᴀʀ (ʜᴇʟᴘ)", callback_data="show_help")],
        [InlineKeyboardButton("👨‍💻 ꜱᴀʜɪʙ", url="https://t.me/kullaniciadidi")],
        [InlineKeyboardButton("➕ ᴍəɴɪ ǫʀᴜᴘᴀ Əʟᴀᴠə ᴇᴅɪɴ", url=f"https://t.me/{context.bot.username}?startgroup=true")],
        [InlineKeyboardButton("📢 ʙᴏᴛ ᴋᴀɴᴀʟı", url="https://t.me/ht_bots"),
         InlineKeyboardButton("💬 ᴋöᴍəᴋ ǫʀᴜᴘᴜ", url="https://t.me/ht_bots_chat")]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.message.reply_text("❌ ʙᴜ ᴋᴏᴍᴀɴᴅᴀ ꜱᴀᴅəᴄə ǫʀᴜᴘ ÜÇÜɴᴅÜʀ!")
        return
    if not await is_admin(update): return
    help_text = (
        "📜 ʙᴏᴛ ᴋᴏᴍᴀɴᴅᴀʟᴀʀı:\n\n"
        "🔹 /on - ʙÜᴛÜɴ ꜱᴛɪᴋᴇʀ ᴠə ɢɪꜰ-ʟəʀɪ ʙᴀĞʟᴀʏıʀ (Qᴜʀᴜᴄᴜ)\n"
        "🔹 /off - ꜱᴛɪᴋᴇʀ ᴠə ɢɪꜰ ɪᴄᴀᴢəꜱɪ ᴠᴇʀɪʀ (Qᴜʀᴜᴄᴜ)\n\n"
        "✨ ꜱöʏÜşʟəʀ ᴀᴠᴛᴏᴍᴀᴛɪᴋ ꜱɪʟɪɴɪʀ!"
    )
    await update.message.reply_text(help_text)

async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.message.chat.type == "private":
        await query.answer("❌ ʙᴜ ᴅÜʏᴍə ꜱᴀᴅəᴄə ǫʀᴜᴘ ÜÇÜɴᴅÜʀ!", show_alert=True)
        return
    if await is_admin(update):
        help_text = (
            "📜 ʙᴏᴛ ᴋᴏᴍᴀɴᴅᴀʟᴀʀı:\n\n"
            "🔹 /on - ʙÜᴛÜɴ ꜱᴛɪᴋᴇʀ ᴠə ɢɪꜰ-ʟəʀɪ ʙᴀĞʟᴀʏıʀ (Qᴜʀᴜᴄᴜ)\n"
            "🔹 /off - ꜱᴛɪᴋᴇʀ ᴠə ɢɪꜰ ɪᴄᴀᴢəꜱɪ ᴠᴇʀɪʀ (Qᴜʀᴜᴄᴜ)\n\n"
            "✨ ꜱöʏÜşʟəʀ ᴀᴠᴛᴏᴍᴀᴛɪᴋ ꜱɪʟɪɴɪʀ!"
        )
        await query.message.edit_text(help_text)
    else:
        await query.answer("❌ ʙᴜunᴜ ꜱᴀᴅəᴄə ᴀᴅᴍɪɴʟəʀ ɢöʀə ʙɪʟəʀ!", show_alert=True)

async def add_banned_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == BOT_OWNER_ID and context.args:
        new_word = " ".join(context.args).lower()
        if new_word not in BANNED_WORDS:
            BANNED_WORDS.append(new_word)
            await update.message.reply_text(f"✅ '{new_word}' ꜱöᴢÜ ʙᴀᴢᴀʏᴀ Əʟᴀᴠə ᴇᴅɪʟᴅɪ.")

async def stiker_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await is_creator(update):
        settings["all_stickers_off"] = True
        await update.message.reply_text("🚫 ʙÜᴛÜɴ ꜱᴛɪᴋᴇʀ ᴠə ɢɪꜰ-ʟəʀ ǫᴀᴅᴀĞᴀɴ ᴇᴅɪʟᴅɪ!")

async def stiker_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await is_creator(update):
        settings["all_stickers_off"] = False
        await update.message.reply_text("✅ ꜱᴛɪᴋᴇʀ ᴠə ɢɪꜰ ɪᴄᴀᴢəꜱɪ ᴠᴇʀɪʟᴅɪ.")

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.from_user: return
    user = update.effective_user
    
    # Stiker filteri
    if settings["all_stickers_off"] and (msg.sticker or msg.animation):
        try: await msg.delete()
        except: pass
        return
        
    # Söyüş filteri
    if msg.text:
        text_lower = msg.text.lower()
        for word in BANNED_WORDS:
            if word in text_lower:
                try:
                    await msg.delete()
                    warning = f"⚠️ {user.mention_html()}, ɴᴏʀᴍᴀʟ ᴅᴀɴışıɴ!"
                    await context.bot.send_message(chat_id=msg.chat_id, text=warning, parse_mode='HTML')
                except: pass
                break

def main():
    TOKEN = "8563159860:AAHpQrxwu4C1DyTgtxcgSrzl6kHUonmD6rY"
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("on", stiker_on))
    app.add_handler(CommandHandler("off", stiker_off))
    app.add_handler(CommandHandler("qadaga", add_banned_word))
    app.add_handler(CallbackQueryHandler(help_callback, pattern="show_help"))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_messages))

    app.run_polling()

if __name__ == "__main__":
    main()
