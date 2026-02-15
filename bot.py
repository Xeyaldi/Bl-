import sys
from types import ModuleType

# --- HEROKU PYTHON 3.13+ XƏTASI ÜÇÜN YAMAQ ---
try:
    import imghdr
except ImportError:
    imghdr = ModuleType('imghdr')
    sys.modules['imghdr'] = imghdr
# ---------------------------------------------

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- AYARLAR ---
BOT_OWNER_ID = 8024893255 
# Sənin göndərdiyin stiker ID-si:
START_STICKER_ID = "CAACAgQAAxkBAAEQhcppkc-7kbd_oDn4S9MV6T5vv-TL9AACQhgAAiRYeVGtiXa89ZuMAzoE"

BANNED_WORDS = [
    "bic", "gic", "peyser", "qodu", "ogras", "fahişe", "sherefsiz", "exlaqsiz", "gicbeser", "meymun", "andira", "zibil", "itoglu", "alcaq", "sherefsiz", "arsiz", "namussuz", "qancıq", "ogras", "tulku", "paxıl", "iyrenc", "mal", "eşşek", "it", "donuz", "heyvan", "qaltax", "qehbe", "bicinbalasi", "soxum", "var-yox", "nəsil", "itoglu", "itqizi", "gicbəsər", "kütbeyin", "şərəfsiz", "ləyaqətsiz", "mənliysiz", "namussuz", "abırsız", "həyasız", "üzsüz", "tərbiyəsiz", "mərifətsiz", "insafsız", "vicdansız", "itbalası", "donuzbalası", "yalançı", "fırıldaqçı", "oğru", "alçaq", "rəzil", "iyrənc", "murdar", "axmaq", "sarsaq", "ədəbsiz", "əxlaqsız", "pozğun", "nadan", "cahil", "qanmaz", "beyinsiz", "gicgah", "xiyar", "balqabaq", "qoyun", "keçi", "eşşək", "vəhşi", "itil", "rəddol"
]

# Hər qrup üçün kilid vəziyyətini yadda saxlayan lüğət
group_locks = {}

async def post_init(application: Application):
    commands = [
        BotCommand("start", "ʙᴏᴛᴜ ʙᴀşʟᴀᴅıɴ"),
        BotCommand("help", "ᴋöᴍəᴋ ᴍᴇɴʏᴜꜱᴜ"),
        BotCommand("on", "ꜱᴛɪᴋᴇʀ ᴠə ɢɪꜰ ʙᴀɢʟᴀ (Qᴜʀᴜᴄᴜ)"),
        BotCommand("off", "ꜱᴛɪᴋᴇʀ ᴠə ɢɪꜰ ᴀᴄ (Qᴜʀᴜᴄᴜ)"),
        BotCommand("qadaga", "ꜱöʏÜş Əʟᴀᴠə ᴇᴛ (Sᴀʜɪʙ)")
    ]
    await application.bot.set_my_commands(commands)

async def is_creator(update: Update):
    if update.effective_chat.type == "private": return True
    member = await update.effective_chat.get_member(update.effective_user.id)
    return member.status == 'creator'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # Mesaja 🗿 reaksiyası verir
    try: await update.message.set_reaction(reaction="🗿")
    except: pass

    # Sənin stikerini göndərir
    try:
        await context.bot.send_sticker(chat_id=chat_id, sticker=START_STICKER_ID)
    except: pass

    text = (
        f"✨ **Sᴀʟᴀᴍ, {user.first_name}!**\n\n"
        f"🛡️ ᴍəɴ **ǫʀᴜᴘʟᴀʀı** ᴛəᴍɪᴢ ꜱᴀxʟᴀʏᴀɴ ✨\n"
        f"🚀 ᴘʀᴏꜰᴇꜱɪʏᴏɴᴀʟ ᴍᴏᴅᴇʀᴀᴛᴏʀ ʙᴏᴛᴀᴍ.\n\n"
        f"💎 **ɴə ᴇᴅə ʙɪʟəʀəᴍ?**\n"
        f"└─ ꜱöʏÜşʟəʀɪ ᴀᴠᴛᴏᴍᴀᴛɪᴋ ᴛəᴍɪᴢʟəʏɪʀəᴍ\n"
        f"└─ ꜱᴛɪᴋᴇʀ ᴠə ɢɪꜰ-ʟəʀɪ ᴍəʜᴅᴜᴅʟᴀşᴅıʀıʀᴀᴍ\n\n"
        f"⚙️ *ʙᴏᴛᴜ ɪşʟəᴛᴍəᴋ ÜÇÜɴ ǫʀᴜᴘᴀ Əʟᴀᴠə ᴇᴅɪʙ ᴀᴅᴍɪɴ ᴠᴇʀɪɴ!*"
    )
    keyboard = [
        [InlineKeyboardButton("📚 ᴋᴏᴍᴀɴᴅᴀʟᴀʀ ᴠə ᴋöᴍəᴋ", callback_data="show_help")],
        [InlineKeyboardButton("👨‍💻 ꜱᴀʜɪʙ", url="https://t.me/kullaniciadidi")],
        [InlineKeyboardButton("➕ ᴍəɴɪ ǫʀᴜᴘᴀ Əʟᴀᴠə ᴇᴅɪɴ", url=f"https://t.me/{context.bot.username}?startgroup=true")],
        [InlineKeyboardButton("📢 ʙᴏᴛ ᴋᴀɴᴀʟı", url="https://t.me/ht_bots"),
         InlineKeyboardButton("💬 ᴋöᴍəᴋ ǫʀᴜᴘᴜ", url="https://t.me/ht_bots_chat")]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def stiker_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.message.reply_text("❌ ʙᴜ ᴋᴏᴍᴀɴᴅᴀ ꜱᴀᴅəᴄə ǫʀᴜᴘ ÜÇÜɴᴅÜʀ!")
        return
    if not await is_creator(update):
        await update.message.reply_text("❌ **ʙᴜ əᴍʀ ʏᴀʟɴıᴢ ǫʀᴜᴘ ǫᴜʀᴜᴄᴜꜱᴜ ÜÇÜɴᴅÜʀ!**", parse_mode="Markdown")
        return
    group_locks[update.effective_chat.id] = True
    await update.message.reply_text("🚫 **ʙᴜ ǫʀᴜᴘᴅᴀ ꜱᴛɪᴋᴇʀ ᴠə ɢɪꜰ-ʟəʀ ǫᴀᴅᴀɢᴀɴ ᴇᴅɪʟᴅɪ!**", parse_mode="Markdown")

async def stiker_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.message.reply_text("❌ ʙᴜ ᴋᴏᴍᴀɴᴅᴀ ꜱᴀᴅəᴄə ǫʀᴜᴘ ÜÇÜɴᴅÜʀ!")
        return
    if not await is_creator(update):
        await update.message.reply_text("❌ **ʙᴜ əᴍʀ ʏᴀʟɴıᴢ ǫʀᴜᴘ ǫᴜʀᴜᴄᴜꜱᴜ ÜÇÜɴᴅÜʀ!**", parse_mode="Markdown")
        return
    group_locks[update.effective_chat.id] = False
    await update.message.reply_text("✅ **ʙᴜ ǫʀᴜᴘᴅᴀ ꜱᴛɪᴋᴇʀ ᴠə ɢɪꜰ ɪᴄᴀᴢəꜱɪ ᴠᴇʀɪʟᴅɪ.**", parse_mode="Markdown")

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.from_user: return
    chat_id = update.effective_chat.id
    
    # Qrup kilidlidirsə həm stiker, həm də gif silinsin
    if group_locks.get(chat_id, False) and (msg.sticker or msg.animation):
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
                    warning = f"⚠️ {update.effective_user.mention_html()}, ɴᴏʀᴍᴀʟ ᴅᴀɴışıɴ!"
                    await context.bot.send_message(chat_id=chat_id, text=warning, parse_mode='HTML')
                except: pass
                break

async def add_banned_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != BOT_OWNER_ID:
        await update.message.reply_text("❌ **ʙᴜ əᴍʀ ʏᴀʟɴıᴢ ʙᴏᴛ ꜱᴀʜɪʙɪ ÜÇÜɴᴅÜʀ!**", parse_mode="Markdown")
        return
    if context.args:
        word = " ".join(context.args).lower()
        if word not in BANNED_WORDS:
            BANNED_WORDS.append(word)
            await update.message.reply_text(f"✅ '{word}' siyahıya əlavə edildi.")

async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    help_text = "📜 **ʙᴏᴛ ᴋᴏᴍᴀɴᴅᴀʟᴀʀı:**\n\n🔹 /on - ꜱᴛɪᴋᴇʀ/ɢɪꜰ ʙᴀɢʟᴀ\n🔹 /off - ꜱᴛɪᴋᴇʀ/ɢɪꜰ ᴀᴄ\n🔹 /qadaga - ꜱöʏÜş Əʟᴀᴠə ᴇᴛ"
    await query.message.edit_text(help_text, parse_mode="Markdown")

def main():
    TOKEN = "8563159860:AAHpQrxwu4C1DyTgtxcgSrzl6kHUonmD6rY"
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("on", stiker_on))
    app.add_handler(CommandHandler("off", stiker_off))
    app.add_handler(CommandHandler("qadaga", add_banned_word))
    app.add_handler(CallbackQueryHandler(help_callback, pattern="show_help"))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_messages))
    
    app.run_polling()

if __name__ == "__main__":
    main() 
