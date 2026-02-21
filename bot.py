İmport sys
from types import ModuleType

# --- HEROKU PYTHON 3.13+ XƏTASI ÜÇÜN YAMAQ ---
try:
    import imghdr
except ImportError:
    imghdr = ModuleType('imghdr')
    sys.modules['imghdr'] = imghdr
# ---------------------------------------------

import logging
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- AYARLAR ---
OWNERS = [8024893255] 
START_STICKER_ID = "CAACAgQAAxkBAAEQhcppkc-7kbd_oDn4S9MV6T5vv-TL9AACQhgAAiRYeVGtiXa89ZuMAzoE"

BANNED_WORDS = []

# Qrup ayarlarını və icazəli istifadəçiləri saxlamaq üçün
group_settings = {} # {chat_id: {"sticker": bool, "voice": bool, "allowed": [user_ids]}}

async def post_init(application: Application):
    commands = [
        BotCommand("start", "ʙᴏᴛᴜ ʙᴀşʟᴀᴅıɴ"),
        BotCommand("help", "ᴋöᴍəᴋ ᴍᴇɴʏᴜꜱᴜ"),
        BotCommand("stiker", "on/off - ꜱᴛɪᴋᴇʀ ᴠə ɢɪꜰ (Qᴜʀᴜᴄᴜ)"),
        BotCommand("seslimesaj", "on/off - ꜱəsʟɪ ᴍᴇsᴀᴊʟᴀʀı ʙᴀɢʟᴀ (Qᴜʀᴜᴄᴜ)"),
        BotCommand("icaze", "İstifadəçiyə yetki ver (Reply)")
    ]
    await application.bot.set_my_commands(commands)

# --- YETKİ YOXLAMA FUNKSİYASI ---
async def has_permission(update: Update):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    # Bot sahibi həmişə yetkilidir
    if user_id in OWNERS: return True
    if update.effective_chat.type == "private": return True
    
    # Qrup qurucusu yoxlanışı
    member = await update.effective_chat.get_member(user_id)
    if member.status == 'creator': return True
    
    # /icaze verilmiş şəxslər
    allowed_users = group_settings.get(chat_id, {}).get("allowed", [])
    if user_id in allowed_users: return True
    
    return False

# --- SAHİB YOXLANILMASI ---
def is_owner(user_id):
    return user_id in OWNERS

# --- OWNER KOMANDALARI ---

async def pisseyler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id): return
    if not BANNED_WORDS:
        await update.message.reply_text("Siyahı hazırda boşdur.")
        return
    siyahı = ", ".join(BANNED_WORDS)
    await update.message.reply_text(f"🚫 Qeyd olunan söyüşlər:\n\n{siyahı}")

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
    
    added_words = []
    already_exists = []
    
    for word in context.args:
        word = word.lower()
        if word not in BANNED_WORDS:
            BANNED_WORDS.append(word)
            added_words.append(word)
        else:
            already_exists.append(word)
    
    response = ""
    if added_words:
        response += f"✅ Əlavə edildi: {', '.join(added_words)}\n"
    if already_exists:
        response += f"⚠️ Zatən var idi: {', '.join(already_exists)}"
        
    await update.message.reply_text(response, parse_mode="Markdown")

async def deleteqeyd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id): return
    if not context.args:
        await update.message.reply_text("İstifadə: `/deleteqeyd söz`")
        return
    
    word = context.args[0].lower()
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
        f"✨ Sᴀʟᴀᴍ, {user.first_name}!\n\n"
        f"🛡️ ᴍəɴ ǫʀᴜᴘʟᴀʀı ᴛəᴍɪᴢ ꜱᴀxʟᴀʏᴀɴ ✨\n"
        f"🚀 ᴘʀᴏꜰᴇꜱɪʏᴏɴᴀʟ ᴍᴏᴅᴇʀᴀᴛᴏʀ ʙᴏᴛᴀᴍ.\n\n"
        f"💎 ɴə ᴇᴅə ʙɪʟəʀəᴍ?\n"
        f"└─ ꜱöʏÜşʟəʀɪ ᴀᴠᴛᴏᴍᴀᴛɪᴋ ᴛəᴍɪᴢʟəʏɪʀəᴍ\n"
        f"└─ ʟɪɴᴋʟəʀɪ ᴀᴠᴛᴏᴍᴀᴛɪᴋ sɪʟɪʀəᴍ\n"
        f"└─ ꜱᴛɪᴋᴇʀ, ɢɪꜰ ᴠə səsʟɪ ᴍəʜᴅᴜᴅʟᴀşᴅıʀıʀᴀᴍ\n\n"
        f"⚙️ ʙᴏᴛᴜ ɪşʟəᴛᴍəᴋ ÜÇÜɴ ǫʀᴜᴘᴀ Əʟᴀᴠə ᴇᴅɪʙ ᴀᴅᴍɪɴ ᴠᴇʀɪɴ!"
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
        help_text = (
            "📜 ʙᴏᴛ ᴋᴏᴍᴀɴᴅᴀʟᴀʀı:\n\n"
            "🔹 /stiker on/off - ꜱᴛɪᴋᴇʀ/ɢɪꜰ ʙʟᴏᴋ\n"
            "🔹 /seslimesaj on/off - Səsli mesaj ʙʟᴏᴋ\n"
            "🔹 /icaze - İstifadəçiyə yetki ver (Reply ilə)\n"
            "📌 Linklər avtomatik silinir."
        )
        await query.message.edit_text(help_text, parse_mode="Markdown")
        
    elif query.data == "owner_menu":
        if not is_owner(user_id):
            await query.answer("❌ Bu menyu yalnız bot sahibləri üçündür!", show_alert=True)
            return
        owner_text = (
            "👑 ꜱᴀʜɪʙ ÖZƏʟ ᴍᴇɴʏᴜꜱᴜ:\n\n"
            "🔹 /pisseyler - Söyüş siyahısını gör\n"
            "🔹 /mesajisil - Reply atılan mesajı sil\n"
            "🔹 /pissozplus - Çoxlu söyüş əlavə et\n"
            "🔹 /deleteqeyd - Siyahıdan söyüş sil"
        )
        await query.message.edit_text(owner_text, parse_mode="Markdown")

# --- YENİ FUNKSİYALAR (STIKER, SESLİ, ICAZE) ---

async def stiker_control(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private": return
    if not await has_permission(update):
        await update.message.reply_text("❌ ʙᴜ ᴋᴏᴍᴀɴᴅᴀ ꜱᴀᴅəᴄə ǫʀᴜᴘ ǫᴜʀᴜᴄᴜꜱᴜ ɪsᴛɪꜰᴀᴅə ᴇᴅə ʙɪʟəʀ!")
        return
    
    chat_id = update.effective_chat.id
    if chat_id not in group_settings: group_settings[chat_id] = {"sticker": False, "voice": False, "allowed": []}
    
    status = context.args[0].lower() if context.args else ""
    if status == "off": # FUNKSIYA YERİ DƏYİŞDİRİLDİ: off artıq bağlayır
        group_settings[chat_id]["sticker"] = True
        await update.message.reply_text("🚫 ʙÜᴛÜɴ ꜱᴛɪᴋᴇʀ ᴠə ɢɪꜰ-ʟəʀ ʙᴀɢʟᴀɴᴅı!")
    elif status == "on": # FUNKSIYA YERİ DƏYİŞDİRİLDİ: on artıq icazə verir
        group_settings[chat_id]["sticker"] = False
        await update.message.reply_text("✅ ꜱᴛɪᴋᴇʀ ᴠə ɢɪꜰ ɪᴄᴀᴢəꜱɪ ᴠᴇʀɪʟᴅɪ.")
    else:
        await update.message.reply_text("İstifadə: `/stiker on` və ya `/stiker off`", parse_mode="Markdown")

async def voice_control(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == "private": return
    if not await has_permission(update):
        await update.message.reply_text("❌ ʙᴜ ᴋᴏᴍᴀɴᴅᴀ ꜱᴀᴅəᴄə ǫʀᴜᴘ ǫᴜʀᴜᴄᴜꜱᴜ ɪsᴛɪꜰᴀᴅə ᴇᴅə ʙɪʟəʀ!")
        return
    
    chat_id = update.effective_chat.id
    if chat_id not in group_settings: group_settings[chat_id] = {"sticker": False, "voice": False, "allowed": []}
    
    status = context.args[0].lower() if context.args else ""
    if status == "off": # Sənin istədiyin kimi /seslimesaj off yazanda silsin
        group_settings[chat_id]["voice"] = True
        await update.message.reply_text("🚫 səsʟɪ ᴍᴇsᴀᴊʟᴀʀ ʙᴀɢʟᴀɴᴅı!")
    elif status == "on":
        group_settings[chat_id]["voice"] = False
        await update.message.reply_text("✅ səsʟɪ ᴍᴇsᴀᴊʟᴀʀᴀ ɪᴄᴀᴢə ᴠᴇʀɪʟᴅɪ.")
    else:
        await update.message.reply_text("İstifadə: `/seslimesaj off` (bağlamaq) və ya `/seslimesaj on` (açmaq)")

async def give_permission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await has_permission(update):
        await update.message.reply_text("❌ Bu komandanı ancaq qurucu işlədə bilər.")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("Yetki vermək üçün istifadəçinin mesajına reply atın.")
        return
    
    chat_id = update.effective_chat.id
    new_user = update.message.reply_to_message.from_user.id
    
    if chat_id not in group_settings: group_settings[chat_id] = {"sticker": False, "voice": False, "allowed": []}
    if new_user not in group_settings[chat_id]["allowed"]:
        group_settings[chat_id]["allowed"].append(new_user)
        await update.message.reply_text(f"✅ {update.message.reply_to_message.from_user.first_name} artıq botu idarə edə bilər.")
    else:
        await update.message.reply_text("Bu şəxs artıq yetkilidir.")

# --- MESAJ İDARƏÇİSİ ---

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.from_user: return
    chat_id = update.effective_chat.id
    user_id = msg.from_user.id
    
    # Qurucu, Sahib və ya İcazəlilərə toxunma
    is_privileged = await has_permission(update)
    
    # 1. Link Silmə (Hər kəs üçün, adminlər xaric)
    if not is_privileged and msg.text:
        links = re.findall(r'(https?://[^\s]+|t\.me/[^\s]+)', msg.text.lower())
        if links:
            try: 
                await msg.delete()
                return
            except: pass

    # 2. Stiker/Gif Blok
    if not is_privileged and group_settings.get(chat_id, {}).get("sticker", False):
        if msg.sticker or msg.animation:
            try: await msg.delete()
            except: pass
            return

    # 3. Səsli Mesaj Blok
    if not is_privileged and group_settings.get(chat_id, {}).get("voice", False):
        if msg.voice or msg.video_note:
            try: await msg.delete()
            except: pass
            return

    # 4. Söyüş Silmə
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
    help_text = "📜 ʙᴏᴛ ᴋᴏᴍᴀɴᴅᴀʟᴀʀı:\n\n🔹 /stiker on/off\n🔹 /seslimesaj on/off\n🔹 /icaze (reply)"
    await update.message.reply_text(help_text, parse_mode="Markdown")

def main():
    TOKEN = "8563159860:AAHpQrxwu4C1DyTgtxcgSrzl6kHUonmD6rY"
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stiker", stiker_control))
    app.add_handler(CommandHandler("seslimesaj", voice_control))
    app.add_handler(CommandHandler("icaze", give_permission))
    
    app.add_handler(CommandHandler("pisseyler", pisseyler))
    app.add_handler(CommandHandler("mesajisil", mesajisil))
    app.add_handler(CommandHandler("pissozplus", pissozplus))
    app.add_handler(CommandHandler("deleteqeyd", deleteqeyd))
    
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_messages))
    
    app.run_polling()

if __name__ == "__main__":
    main()
