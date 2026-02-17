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
START_STICKER_ID = "CAACAgQAAxkBAAEQhcppkc-7kbd_oDn4S9MV6T5vv-TL9AACQhgAAiRYeVGtiXa89ZuMAzoE"

BANNED_WORDS = [
    "bic", "gic", "peyser", "qodu", "ogras", "fahişe", "sherefsiz", "exlaqsiz", "gicbeser", "meymun", "andira", "zibil", "itoglu", "alcaq", "sherefsiz", "arsiz", "namussuz", "qancıq", "ogras", "tulku", "paxıl", "iyrenc", "mal", "eşşek", "it", "donuz", "heyvan", "qaltax", "qehbe", "bicinbalasi", "soxum", "var-yox", "nəsil", "itoglu", "itqizi", "gicbəsər", "kütbeyin", "şərəfsiz", "ləyaqətsiz", "mənliysiz", "namussuz", "abırsız", "həyasız", "üzsüz", "tərbiyəsiz", "mərifətsiz", "insafsız", "vicdansız", "itbalası", "donuzbalası", "yalançı", "fırıldaqçı", "oğru", "alçaq", "rəzil", "iyrənc", "murdar", "axmaq", "sarsaq", "ədəbsiz", "əxlaqsız", "pozğun", "nadan", "cahil", "qanmaz", "beyinsiz", "gicgah", "xiyar", "balqabaq", "qoyun", "keçi", "eşşək", "vəhşi", "itil", "rəddol"
]

group_locks = {}

async def post_init(application: Application):
    commands = [
        BotCommand("start", "ʙᴏᴛᴜ ʙᴀşʟᴀᴅıɴ"),
        BotCommand("help", "ᴋöᴍəᴋ ᴍᴇɴʏᴜꜱᴜ"),
        BotCommand("on", "ꜱᴛɪᴋᴇʀ ᴠə ɢɪꜰ ʙᴀɢʟᴀ (Qᴜʀᴜᴄᴜ)"),
        BotCommand("off", "ꜱᴛɪᴋᴇʀ ᴠə ɢɪꜰ ᴀᴄ (Qᴜʀᴜᴄᴜ)")
    ]
    await application.bot.set_my_commands(commands)

async def is_creator(update: Update):
    if update.effective_chat.type == "private": return True
    member = await update.effective_chat.get_member(update.effective_user.id)
    return member.status == 'creator'

# --- YENİ OWNER KOMANDALARI ---

async def pisseyler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != BOT_OWNER_ID: return
    siyahı = ", ".join(BANNED_WORDS)
    await update.message.reply_text(f"🚫 **Qeyd olunan söyüşlər:**\n\n{siyahı}")

async def mesajisil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != BOT_OWNER_ID: return
    if not update.message.reply_to_message:
        await update.message.reply_text("Silmək üçün bir mesaja reply (cavab) atın.")
        return
    try:
        await update.message.reply_to_message.delete()
        await update.message.delete()
    except: pass

async def pissözplus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != BOT_OWNER_ID: return
    if not context.args:
        await update.message.reply_text("İstifadə: `/pissözplus söyüş`", parse_mode="Markdown")
        return
    word = " ".join(context.args).lower()
    if word not in BANNED_WORDS:
        BANNED_WORDS.append(word)
        await update.message.reply_text(f"✅ '{word}' siyahıya əlavə edildi.")
    else:
        await update.message.reply_text("Bu söz artıq siyahıda var.")

async def deleteqeyd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != BOT_OWNER_ID: return
    if not context.args:
        await update.message.reply_text("İstifadə: `/deleteqeyd söyüş`", parse_mode="Markdown")
        return
    word = " ".join(context.args).lower()
    if word in BANNED_WORDS:
        BANNED_WORDS.remove(word)
        await update.message.reply_text(f"🗑️ '{word}' siyahıdan silindi.")
    else:
        await update.message.reply_text("Bu söz siyahıda tapılmadı.")

# --- START VƏ BUTONLAR ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    try: await update.message.set_reaction(reaction="🗿")
    except: pass
    try: await context.bot.send_sticker(chat_id=chat_id, sticker=START_STICKER_ID)
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
        [InlineKeyboardButton("👑 ꜱᴀʜɪʙ ᴋᴏᴍᴜᴛʟᴀʀı", callback_data="owner_menu")],
        [InlineKeyboardButton("👨‍💻 ꜱᴀʜɪʙ", url="https://t.me/kullaniciadidi")],
        [InlineKeyboardButton("➕ ᴍəɴɪ ǫʀᴜᴘᴀ Əʟᴀᴠə ᴇᴅɪɴ", url=f"https://t.me/{context.bot.username}?startgroup=true")],
        [InlineKeyboardButton("📢 ʙᴏᴛ ᴋᴀɴᴀʟı", url="https://t.me/ht_bots"),
         InlineKeyboardButton("💬 ᴋöᴍəᴋ ǫʀᴜᴘᴜ", url="https://t.me/ht_bots_chat")]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    
    if query.data == "show_help":
        help_text = "📜 **ʙᴏᴛ ᴋᴏᴍᴀɴᴅᴀʟᴀʀı:**\n\n🔹 /on - ꜱᴛɪᴋᴇʀ/ɢɪꜰ ʙᴀɢʟᴀ (Qᴜʀᴜᴄᴜ)\n🔹 /off - ꜱᴛɪᴋᴇʀ/ɢɪꜰ ᴀᴄ (Qᴜʀᴜᴄᴜ)"
        await query.message.edit_text(help_text, parse_mode="Markdown")
        
    elif query.data == "owner_menu":
        if user_id != BOT_OWNER_ID:
            await query.answer("❌ Bu menyu yalnız bot sahibi üçündür!", show_alert=True)
            return
        owner_text = (
            "👑 **ꜱᴀʜɪʙ ÖZƏʟ ᴍᴇɴʏᴜꜱᴜ:**\n\n"
            "🔹 /pisseyler - Söyüş siyahısını gör\n"
            "🔹 /mesajisil - Reply atılan mesajı sil\n"
            "🔹 /pissözplus - Siyahıya söyüş əlavə et\n"
            "🔹 /deleteqeyd - Siyahıdan söyüş sil"
        )
        await query.message.edit_text(owner_text, parse_mode="Markdown")

# --- DİGƏR FUNKSİYALAR ---

async def stiker_on(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.message.reply_text("❌ ʙᴜ ᴋᴏᴍᴀɴᴅᴀ ꜱᴀᴅəᴄə ǫʀᴜᴘ ÜÇÜɴᴅÜʀ!")
        return
    if not await is_creator(update):
        await update.message.reply_text("❌ **ʙᴜ əᴍʀ ʏᴀʟɴıᴢ ǫᴜʀᴜᴄᴜ ÜÇÜɴᴅÜʀ!**", parse_mode="Markdown")
        return
    group_locks[update.effective_chat.id] = True
    await update.message.reply_text("🚫 **ʙÜᴛÜɴ ꜱᴛɪᴋᴇʀ ᴠə ɢɪꜰ-ʟəʀ ʙᴀɢʟᴀɴᴅı!**", parse_mode="Markdown")

async def stiker_off(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private":
        await update.message.reply_text("❌ ʙᴜ ᴋᴏᴍᴀɴᴅᴀ ꜱᴀᴅəᴄə ǫʀᴜᴘ ÜÇÜɴᴅÜʀ!")
        return
    if not await is_creator(update):
        await update.message.reply_text("❌ **ʙᴜ əᴍʀ ʏᴀʟɴıᴢ ǫᴜʀᴜᴄᴜ ÜÇÜɴᴅÜʀ!**", parse_mode="Markdown")
        return
    group_locks[update.effective_chat.id] = False
    await update.message.reply_text("✅ **ꜱᴛɪᴋᴇʀ ᴠə ɢɪꜰ ɪᴄᴀᴢəꜱɪ ᴠᴇʀɪʟᴅɪ.**", parse_mode="Markdown")

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.from_user: return
    chat_id = update.effective_chat.id
    
    if group_locks.get(chat_id, False) and (msg.sticker or msg.animation):
        try: await msg.delete()
        except: pass
        return

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

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = "📜 **ʙᴏᴛ ᴋᴏᴍᴀɴᴅᴀʟᴀʀı:**\n\n🔹 /on - ꜱᴛɪᴋᴇʀ/ɢɪꜰ ʙᴀɢʟᴀ (Qᴜʀᴜᴄᴜ)\n🔹 /off - ꜱᴛɪᴋᴇʀ/ɢɪꜰ ᴀᴄ (Qᴜʀᴜᴄᴜ)"
    await update.message.reply_text(help_text, parse_mode="Markdown")

def main():
    TOKEN = "8563159860:AAHpQrxwu4C1DyTgtxcgSrzl6kHUonmD6rY"
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("on", stiker_on))
    app.add_handler(CommandHandler("off", stiker_off))
    
    # Owner Komandaları
    app.add_handler(CommandHandler("pisseyler", pisseyler))
    app.add_handler(CommandHandler("mesajisil", mesajisil))
    app.add_handler(CommandHandler("pissözplus", pissözplus))
    app.add_handler(CommandHandler("deleteqeyd", deleteqeyd))
    app.add_handler(CommandHandler("qadaga", pissözplus)) # Köhnə funksiyanı saxladım
    
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_messages))
    
    app.run_polling()

if __name__ == "__main__":
    main()
