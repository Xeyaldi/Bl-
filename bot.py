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
OWNERS = [8024893255]
START_STICKER_ID = "CAACAgQAAxkBAAEQhcppkc-7kbd_oDn4S9MV6T5vv-TL9AACQhgAAiRYeVGtiXa89ZuMAzoE"

BANNED_WORDS = []

# Yaddaş sistemi (Stiker, Səsli və İcazəli istifadəçilər üçün)
group_locks = {}

def get_chat_settings(chat_id):
    if chat_id not in group_locks:
        group_locks[chat_id] = {
            'stiker_lock': False,
            'sesli_lock': False,
            'authorized_users': []
        }
    return group_locks[chat_id]

async def post_init(application: Application):
    commands = [
        BotCommand("start", "ʙᴏᴛᴜ ʙᴀşʟᴀᴅıɴ"),
        BotCommand("help", "ᴋöᴍəᴋ ᴍᴇɴʏᴜꜱᴜ"),
        BotCommand("stiker", "ꜱᴛɪᴋᴇʀ ᴠə ɢɪꜰ ᴀᴄ/ʙᴀɢʟᴀ (ᴏɴ/ᴏꜰꜰ)"),
        BotCommand("seslimesaj", "ꜱəꜱʟɪ ᴍᴇꜱᴀᴊ ᴀᴄ/ʙᴀɢʟᴀ (ᴏɴ/ᴏꜰꜰ)"),
        BotCommand("icaze", "ʏᴇᴛᴋɪ ᴠᴇʀ (ʀᴇᴘʟʏ ɪʟə)")
    ]
    await application.bot.set_my_commands(commands)

async def has_permission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private": return True
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    member = await update.effective_chat.get_member(user_id)
    
    # Qurucu, Sahiblər siyahısında olanlar və ya /icaze verilmişlər
    if member.status == 'creator' or user_id in OWNERS or user_id in get_chat_settings(chat_id)['authorized_users']:
        return True
    return False

def is_owner(user_id):
    return user_id in OWNERS

# --- YENİ KOMANDALAR ---

async def icaze_ver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private": return
    chat_id = update.effective_chat.id
    member = await update.effective_chat.get_member(update.effective_user.id)
    
    if member.status != 'creator' and update.effective_user.id not in OWNERS:
        await update.message.reply_text("❌ **ʙᴜ ᴋᴏᴍᴀɴᴅᴀ ꜱᴀᴅəᴄə ǫʀᴜᴘ ǫᴜʀᴜᴄᴜꜱᴜ ÜÇÜɴᴅÜʀ!**")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ **ʏᴇᴛᴋɪ ᴠᴇʀᴍəᴋ ÜÇÜɴ ɪꜱᴛɪꜰᴀᴅəÇɪɴɪɴ ᴍᴇꜱᴀᴊıɴᴀ ᴄᴀᴠᴀʙ (ʀᴇᴘʟʏ) ᴠᴇʀɪɴ!**")
        return

    target_id = update.message.reply_to_message.from_user.id
    settings = get_chat_settings(chat_id)
    
    if target_id not in settings['authorized_users']:
        settings['authorized_users'].append(target_id)
        await update.message.reply_text(f"✅ {update.message.reply_to_message.from_user.mention_html()} **ᴀʀᴛıǫ ʙᴏᴛ ᴋᴏᴍᴀɴᴅᴀʟᴀʀıɴı ɪşʟəᴅə ʙɪʟəʀ!**", parse_mode='HTML')
    else:
        await update.message.reply_text("ℹ️ **ʙᴜ ɪꜱᴛɪꜰᴀᴅəÇɪ ᴀʀᴛıǫ ʏᴇᴛᴋɪʟɪᴅɪʀ.**")

async def stiker_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await has_permission(update, context):
        await update.message.reply_text("❌ **ʙᴜ ᴋᴏᴍᴀɴᴅᴀ ꜱᴀᴅəᴄə ǫʀᴜᴘ ǫᴜʀᴜᴄᴜꜱᴜ/ʏᴇᴛᴋɪʟɪ ɪꜱᴛɪꜰᴀᴅə ᴇᴅə ʙɪʟəʀ!**")
        return
    
    chat_id = update.effective_chat.id
    settings = get_chat_settings(chat_id)
    
    if context.args and context.args[0].lower() == "on":
        settings['stiker_lock'] = False
        await update.message.reply_text("✅ **ꜱᴛɪᴋᴇʀ ᴠə ɢɪꜰ ɪᴄᴀᴢəꜱɪ ᴠᴇʀɪʟᴅɪ.**")
    elif context.args and context.args[0].lower() == "off":
        settings['stiker_lock'] = True
        await update.message.reply_text("🚫 **ʙÜᴛÜɴ ꜱᴛɪᴋᴇʀ ᴠə ɢɪꜰ-ʟəʀ ʙᴀɢʟᴀɴᴅı!**")
    else:
        await update.message.reply_text("⚠️ **ɪꜱᴛɪꜰᴀᴅə:** `/stiker on` ᴠə ʏᴀ `/stiker off`", parse_mode="Markdown")

async def sesli_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await has_permission(update, context):
        await update.message.reply_text("❌ **ʙᴜ ᴋᴏᴍᴀɴᴅᴀ ꜱᴀᴅəᴄə ǫʀᴜᴘ ǫᴜʀᴜᴄᴜꜱᴜ/ʏᴇᴛᴋɪʟɪ ɪꜱᴛɪꜰᴀᴅə ᴇᴅə ʙɪʟəʀ!**")
        return
    
    chat_id = update.effective_chat.id
    settings = get_chat_settings(chat_id)
    
    if context.args and context.args[0].lower() == "on":
        settings['sesli_lock'] = False
        await update.message.reply_text("✅ **ꜱəꜱʟɪ ᴍᴇꜱᴀᴊʟᴀʀ ᴀᴋᴛɪᴠ ᴇᴅɪʟᴅɪ.**")
    elif context.args and context.args[0].lower() == "off":
        settings['sesli_lock'] = True
        await update.message.reply_text("🚫 **ꜱəꜱʟɪ ᴍᴇꜱᴀᴊʟᴀʀ ʙᴀɢʟᴀɴᴅı!**")
    else:
        await update.message.reply_text("⚠️ **ɪꜱᴛɪꜰᴀᴅə:** `/seslimesaj on` ᴠə ʏᴀ `/seslimesaj off`", parse_mode="Markdown")

# --- OWNER KOMANDALARI ---

async def pisseyler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id): return
    if not BANNED_WORDS:
        await update.message.reply_text("Siyahı hazırda boşdur.")
        return
    siyahı = ", ".join(BANNED_WORDS)
    await update.message.reply_text(f"🚫 **Qeyd olunan söyüşlər:**\n\n{siyahı}")

async def mesajisil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id): return
    if not update.message.reply_to_message:
        await update.message.reply_text("Silmək üçün bir mesaja reply (cavab) atın.")
        return
    try:
        await update.message.reply_to_message.delete()
        await update.message.delete()
    except: pass

async def pissozplus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id): return
    if not context.args:
        await update.message.reply_text("İstifadə: `/pissozplus söz1 söz2 ...`")
        return
    added_words = [word.lower() for word in context.args if word.lower() not in BANNED_WORDS]
    for w in added_words: BANNED_WORDS.append(w)
    await update.message.reply_text(f"✅ **Əlavə edildi:** {', '.join(added_words)}" if added_words else "⚠️ Sözlər artıq var idi.")

async def deleteqeyd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id): return
    if not context.args: return
    word = context.args[0].lower()
    if word in BANNED_WORDS:
        BANNED_WORDS.remove(word)
        await update.message.reply_text(f"🗑️ '{word}' silindi.")

# --- START VƏ BUTONLAR ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    try: await context.bot.send_sticker(chat_id=update.effective_chat.id, sticker=START_STICKER_ID)
    except: pass
    text = (f"✨ **Sᴀʟᴀᴍ, {user.first_name}!**\n\n🛡️ ᴍəɴ **ǫʀᴜᴘʟᴀʀı** ᴛəᴍɪᴢ ꜱᴀxʟᴀʏᴀɴ ʙᴏᴛᴀᴍ.\n\n"
            f"🔹 /stiker off - Stikerləri bağlayır\n🔹 /seslimesaj off - Səslini bağlayır\n"
            f"🔹 /icaze - Başqasına yetki verir")
    keyboard = [[InlineKeyboardButton("➕ ᴍəɴɪ ǫʀᴜᴘᴀ Əʟᴀᴠə ᴇᴅɪɴ", url=f"https://t.me/{context.bot.username}?startgroup=true")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.from_user: return
    chat_id = update.effective_chat.id
    settings = get_chat_settings(chat_id)
    
    # 1. Link silmə (Admin və yetkililər istisnadır)
    if msg.text or msg.caption:
        content = (msg.text or msg.caption).lower()
        links = ["http://", "https://", "t.me/", "www.", ".com", ".net", ".org", ".az"]
        if any(link in content for link in links):
            if not await has_permission(update, context):
                try: await msg.delete()
                except: pass
                return

    # 2. Söyüş yoxlanışı
    if msg.text:
        text_lower = msg.text.lower()
        for word in BANNED_WORDS:
            if word in text_lower:
                try: 
                    await msg.delete()
                    await context.bot.send_message(chat_id=chat_id, text=f"⚠️ {update.effective_user.mention_html()}, ɴᴏʀᴍᴀʟ ᴅᴀɴışıɴ!", parse_mode='HTML')
                except: pass
                return

    # 3. Stiker/GIF silmə
    if (msg.sticker or msg.animation) and settings['stiker_lock']:
        if not await has_permission(update, context):
            try: await msg.delete()
            except: pass
            return

    # 4. Səsli mesaj / Video mesaj silmə
    if (msg.voice or msg.video_note) and settings['sesli_lock']:
        if not await has_permission(update, context):
            try: await msg.delete()
            except: pass
            return

def main():
    TOKEN = "8563159860:AAHpQrxwu4C1DyTgtxcgSrzl6kHUonmD6rY"
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stiker", stiker_toggle))
    app.add_handler(CommandHandler("seslimesaj", sesli_toggle))
    app.add_handler(CommandHandler("icaze", icaze_ver))
    
    app.add_handler(CommandHandler("pisseyler", pisseyler))
    app.add_handler(CommandHandler("mesajisil", mesajisil))
    app.add_handler(CommandHandler("pissozplus", pissozplus))
    app.add_handler(CommandHandler("deleteqeyd", deleteqeyd))
    
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_messages))
    
    app.run_polling()

if __name__ == "__main__":
    main()
