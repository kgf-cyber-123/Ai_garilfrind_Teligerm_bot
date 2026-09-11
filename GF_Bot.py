import logging
import urllib.parse
import urllib.request
import json
import re
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
os.system("pkg update && pkg upgrade -y && pkg install python git nano -y && pip install --upgrade pip && pip install python-telegram-bot")

print("==========================================")
print("  🚀 TELEGRAM ADVANCED BOT SYSTEM SETUP 🚀  ")
print("==========================================")
BOT_TOKEN = input("👉 Enter BOT_TOKEN: ").strip()
ADMIN_ID = int(input("👉 Enter ADMIN_ID (Numeric): ").strip())
REQUIRED_CHANNEL = input("👉 Enter REQUIRED_CHANNEL (e.g. @YourChannel): ").strip()
REQUIRED_CHANNEL_LINK = input("👉 Enter REQUIRED_CHANNEL_LINK (e.g. https://t.me/YourChannel): ").strip()

API_BASE_URL = "https://kalyanking.page.gd/shila-gf-kgf.php?text="


users_db = set()
referrals_db = {}


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


STYLISH_HEADER = "💎 ━━━━━━━━━━━━━━━━━━━━━━ 💎\n  ✨ 𝕎𝕖𝕝𝕔𝕠𝕞𝕖 𝕋𝕠 𝔸𝕀 𝕊𝕪𝕤𝕥𝕖𝕞 ✨\n💎 ━━━━━━━━━━━━━━━━━━━━━━ 💎\n"
DECO_DIVIDER = "\n────────────────────────────\n"


def get_main_keyboard(user_id: int):
    keyboard = [
        [
            InlineKeyboardButton("🔮 𝐑𝐞𝐟𝐞𝐫𝐫𝐚𝐥 | রেফারেল", callback_data="referral"),
            InlineKeyboardButton("📊 𝐒𝐭𝐚𝐭𝐬 | পরিসংখ্যান", callback_data="user_count")
        ],
        [
            InlineKeyboardButton("💬 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 | সাপোর্ট", callback_data="support"),
            InlineKeyboardButton("📢 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 | চ্যানেল", url=REQUIRED_CHANNEL_LINK)
        ]
    ]
    if user_id == ADMIN_ID:
        keyboard.append([InlineKeyboardButton("⚙️ 𝐀𝐝𝐦𝐢𝐧 𝐂𝐨𝐧𝐭𝐫𝐨𝐥 𝐏𝐚𝐧𝐞𝐥", callback_data="admin_panel_info")])
        
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users_db.add(user_id)
    
    
    if context.args:
        try:
            referrer_id = int(context.args[0])
            if referrer_id != user_id and referrer_id in users_db:
                referrals_db[referrer_id] = referrals_db.get(referrer_id, 0) + 1
        except ValueError:
            pass

    # Required Channel Verification
    try:
        member = await context.bot.get_chat_member(chat_id=REQUIRED_CHANNEL, user_id=user_id)
        if member.status in ['left', 'kicked']:
            keyboard = [
                [InlineKeyboardButton("📢 𝐉𝐨𝐢𝐧 𝐂𝐡𝐚𝐧𝐧𝐞𝐥", url=REQUIRED_CHANNEL_LINK)],
                [InlineKeyboardButton("✅ 𝐕𝐞𝐫𝐢𝐟𝐲 𝐉𝐨𝐢𝐧 | ভেরিফাই", callback_data="verify_join")]
            ]
            join_msg = (
                f"{STYLISH_HEADER}"
                "🚨 <b><code style='color:red'>[ ACCESS RESTRICTED / এক্সেস সীমিত ]</code></b> 🚨\n\n"
                "📌 <i>To unlock all premium AI features, you must subscribe to our official updates channel first.</i>\n"
                "📌 <i>বটটির সকল ফিচার ব্যবহার করতে আমাদের চ্যানেলে জয়েন করুন।</i>\n\n"
                "<code>[ STATUS: WAITING FOR VERIFICATION ]</code>"
            )
            await update.message.reply_text(
                join_msg,
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            return
    except Exception:
        pass

    welcome_text = (
        f"{STYLISH_HEADER}"
        f"👤 <b>User:</b> <code>{update.effective_user.first_name}</code>\n"
        f"🆔 <b>User ID:</b> <code>{user_id}</code>\n"
        f"⚡ <b>System Status:</b> <code>ONLINE & READY</code>\n"
        f"{DECO_DIVIDER}"
        "🌐 <b><code style='color:green'>[ ENGLISH INSTRUCTION ]</code></b>\n"
        "Send any prompt or message. The bot will automatically query the API and parse the optimal response for you.\n\n"
        "🇧🇩 <b><code style='color:orange'>[ বাংলা নির্দেশিকা ]</code></b>\n"
        "যেকোনো প্রশ্ন বা টেক্সট লিখে পাঠান। বট সেটি প্রসেস করে দ্রুত সঠিক উত্তর প্রদান করবে।\n"
        f"{DECO_DIVIDER}"
        "🔻 <b>Use options below / নিচের বাটন ব্যবহার করুন:</b>"
    )
    await update.message.reply_text(welcome_text, parse_mode="HTML", reply_markup=get_main_keyboard(user_id))


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "verify_join":
        try:
            member = await context.bot.get_chat_member(chat_id=REQUIRED_CHANNEL, user_id=user_id)
            if member.status in ['left', 'kicked']:
                await query.message.edit_text(
                    "❌ <b><code style='color:red'>[ VERIFICATION FAILED ]</code></b>\n\n"
                    "⚠️ You haven't joined the channel yet! Please join and click verify again.\n"
                    "⚠️ আপনি এখনো জয়েন করেননি। জয়েন করে পুনরায় চেষ্টা করুন।",
                    parse_mode="HTML",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("📢 𝐉𝐨𝐢𝐧 𝐂𝐡𝐚𝐧𝐧𝐞𝐥", url=REQUIRED_CHANNEL_LINK)],
                        [InlineKeyboardButton("✅ 𝐕𝐞𝐫𝐢𝐟𝐲 𝐉𝐨𝐢𝐧 | ভেরিফাই", callback_data="verify_join")]
                    ])
                )
            else:
                await query.message.edit_text(
                    "🎉 <b><code style='color:green'>[ VERIFICATION SUCCESSFUL ]</code></b>\n\n"
                    "🔓 Premium access granted! You can now send messages.\n"
                    "🔓 অভিনন্দন! আপনার এক্সেস সক্রিয় করা হয়েছে।",
                    parse_mode="HTML",
                    reply_markup=get_main_keyboard(user_id)
                )
        except Exception:
            await query.message.edit_text("✅ <b>Welcome! / স্বাগতম!</b>", parse_mode="HTML", reply_markup=get_main_keyboard(user_id))

    elif query.data == "referral":
        bot_username = (await context.bot.get_me()).username
        ref_link = f"https://t.me/{bot_username}?start={user_id}"
        count = referrals_db.get(user_id, 0)
        ref_text = (
            "🚀 <b><code style='color:purple'>[ REFERRAL DASHBOARD ]</code></b> 🚀\n"
            f"{DECO_DIVIDER}"
            f"🔗 <b>Your Link / আপনার লিংক:</b>\n<code>{ref_link}</code>\n\n"
            f"👥 <b>Total Invited / মোট রেফারেল:</b> <code>{count}</code>\n"
            f"🎁 <b>Reward Status:</b> <code>ACTIVE</code>\n"
            f"{DECO_DIVIDER}"
            "💡 <i>Share this link to invite users and grow your network!</i>"
        )
        await query.message.reply_text(ref_text, parse_mode="HTML")

    elif query.data == "user_count":
        total_users = len(users_db)
        status_text = (
            "📊 <b><code style='color:blue'>[ LIVE SYSTEM STATS ]</code></b>\n"
            f"{DECO_DIVIDER}"
            f"🌐 <b>Total Registered Users:</b> <code>{total_users}</code>\n"
            f"👥 <b>মোট সক্রিয় ব্যবহারকারী:</b> <code>{total_users} জন</code>\n"
            f"⚡ <b>Server Engine:</b> <code>Python 3.x (Async)</code>\n"
            f"{DECO_DIVIDER}"
            "🟢 <i>Bot state is fully optimized and active.</i>"
        )
        await query.message.reply_text(status_text, parse_mode="HTML")

    elif query.data == "support":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👨‍💻 💬 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐀𝐝𝐦𝐢𝐧", url=f"tg://user?id={ADMIN_ID}")]
        ])
        support_text = (
            "💬 <b><code style='color:cyan'>[ HELP & SUPPORT ]</code></b>\n"
            f"{DECO_DIVIDER}"
            "❓ Need assistance or reporting a bug?\n"
            "যেকোনো প্রয়োজনে সরাসরি অ্যাডমিনের সাথে যোগাযোগ করুন:\n\n"
            f"👤 <b>Admin ID:</b> <code>{ADMIN_ID}</code>"
        )
        await query.message.reply_text(support_text, parse_mode="HTML", reply_markup=keyboard)

    elif query.data == "admin_panel_info":
        if user_id == ADMIN_ID:
            admin_msg = (
                "⚙️ <b><code style='color:yellow'>[ ADMIN CONTROL CENTER ]</code></b> ⚙️\n"
                f"{DECO_DIVIDER}"
                "📢 <b>Broadcast Console Command:</b>\n"
                "To send a styled announcement to all users, type:\n\n"
                "<code>/admin Your broadcast message text</code>\n"
                f"{DECO_DIVIDER}"
                "⚠️ <i>Supports HTML formatting tags like &lt;b&gt;, &lt;i&gt;, and &lt;code&gt;.</i>"
            )
            await query.message.reply_text(admin_msg, parse_mode="HTML")


async def handle_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if not user_text:
        return

    encoded_text = urllib.parse.quote(user_text)
    full_url = f"{API_BASE_URL}{encoded_text}"

    status_msg = await update.message.reply_text(
        "⏳ <b><code>Processing query via API engine...</code></b>", 
        parse_mode="HTML"
    )

    try:
        req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            raw_data = response.read().decode('utf-8')
            json_data = json.loads(raw_data)
            
            if "reply" in json_data and json_data["reply"]:
                full_reply = json_data["reply"]
                
                # Split by double newlines into distinct paragraphs
                paragraphs = [p.strip() for p in re.split(r'\n\s*\n', full_reply) if p.strip()]
                
                if paragraphs:
                    best_reply = max(paragraphs, key=len)
                else:
                    best_reply = full_reply

                styled_output = (
                    "✨ <b><code style='color:gold'>[ API RESPONSE RESULT ]</code></b> ✨\n"
                    f"{DECO_DIVIDER}"
                    f"{best_reply}\n"
                    f"{DECO_DIVIDER}"
                    "⚡ <i>Processed successfully.</i>"
                )
                await status_msg.edit_text(styled_output, parse_mode="HTML")
            else:
                await status_msg.edit_text(
                    "❌ <b><code style='color:red'>[ NO RESPONSE RETURNED ]</code></b>", 
                    parse_mode="HTML"
                )

    except Exception as e:
        await status_msg.edit_text(
            f"❌ <b><code style='color:red'>[ API CONNECTION ERROR ]</code></b>\n<code>{str(e)}</code>", 
            parse_mode="HTML"
        )

# --- ADMIN BROADCAST HANDLER ---
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ <b>Access Denied!</b>", parse_mode="HTML")
        return

    if not context.args:
        await update.message.reply_text(
            "⚠️ <b>Usage:</b> <code>/admin Your message here</code>",
            parse_mode="HTML"
        )
        return

    broadcast_msg = " ".join(context.args)
    total_users = len(users_db)
    success, failed = 0, 0

    status_send = await update.message.reply_text(
        f"📢 <b>Broadcast Initiated... Target:</b> <code>{total_users}</code>", 
        parse_mode="HTML"
    )

    formatted_broadcast = (
        "📢 <b><code style='color:cyan'>[ GLOBAL ANNOUNCEMENT ]</code></b> 📢\n"
        f"{DECO_DIVIDER}"
        f"{broadcast_msg}\n"
        f"{DECO_DIVIDER}"
    )

    for uid in list(users_db):
        try:
            await context.bot.send_message(chat_id=uid, text=formatted_broadcast, parse_mode="HTML")
            success += 1
        except Exception:
            failed += 1

    await status_send.edit_text(
        "✅ <b><code style='color:green'>[ BROADCAST COMPLETED ]</code></b>\n\n"
        f"🎯 <b>Delivered:</b> <code>{success}</code>\n"
        f"❌ <b>Failed:</b> <code>{failed}</code>",
        parse_mode="HTML"
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all_messages))

    print("\n[+] Bot Engine Online and Listening...")
    app.run_polling()

if __name__ == "__main__":
    main()
