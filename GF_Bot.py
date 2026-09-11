#____ KGF CYBER TEAM 
#___ BOT CODING :- 
import os

os.system("pip install python-telegram-bot")

import logging
import urllib.parse
import urllib.request
import json
import re
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

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
user_languages = {}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

STYLISH_HEADER = "💎 ━━━━━━━━━━━━━━━━━━━━━━ 💎\n  ✨ 𝕎𝕖𝕝𝕔𝕠𝕞𝕖 𝕋𝕠 𝔸𝕀 𝕊𝕪𝕤𝕥𝕖𝕞 ✨\n💎 ━━━━━━━━━━━━━━━━━━━━━━ 💎\n"
DECO_DIVIDER = "\n────────────────────────────\n"

def get_language_keyboard():
    keyboard = [
        [KeyboardButton("🇧🇩 বাংলা (Bengali)")],
        [KeyboardButton("🇬🇧 English")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_main_keyboard(user_id: int):
    lang = user_languages.get(user_id, 'bn')
    
    if lang == 'bn':
        keyboard = [
            [KeyboardButton("🔮 রেফারেল dashboard")],
            [KeyboardButton("📊 বট পরিসংখ্যান")],
            [KeyboardButton("💬 সাপোর্ট সাহায্য")],
            [KeyboardButton("📢 আমাদের চ্যানেল")],
            [KeyboardButton("🌐 ভাষা পরিবর্তন করুন")]
        ]
        if user_id == ADMIN_ID:
            keyboard.append([KeyboardButton("⚙️ এডমিন প্যানেল")])
    else:
        keyboard = [
            [KeyboardButton("🔮 Referral Dashboard")],
            [KeyboardButton("📊 Bot Statistics")],
            [KeyboardButton("💬 Support & Help")],
            [KeyboardButton("📢 Official Channel")],
            [KeyboardButton("🌐 Change Language")]
        ]
        if user_id == ADMIN_ID:
            keyboard.append([KeyboardButton("⚙️ Admin Panel")])
        
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

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

    if user_id not in user_languages:
        lang_text = (
            f"{STYLISH_HEADER}"
            "👋 <b>Welcome! / স্বাগতম!</b>\n\n"
            "Please select your preferred language below:\n"
            "অনুগ্রহ করে নিচে আপনার পছন্দনীয় ভাষা নির্বাচন করুন:"
        )
        await update.message.reply_text(lang_text, parse_mode="HTML", reply_markup=get_language_keyboard())
        return

    await send_main_welcome(update, context, user_id)

async def send_main_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    lang = user_languages.get(user_id, 'bn')

    try:
        member = await context.bot.get_chat_member(chat_id=REQUIRED_CHANNEL, user_id=user_id)
        if member.status in ['left', 'kicked']:
            if lang == 'bn':
                join_keyboard = ReplyKeyboardMarkup([
                    [KeyboardButton("📢 চ্যানেল দেখুন")],
                    [KeyboardButton("✅ ভেরিফাই জয়েন")]
                ], resize_keyboard=True)
                join_msg = (
                    f"{STYLISH_HEADER}"
                    "🚨 <b>[ এক্সেস সীমিত ]</b> 🚨\n\n"
                    f"📌 <i>আমাদের অফিশিয়াল চ্যানেল লিংক: {REQUIRED_CHANNEL_LINK}</i>\n"
                    "📌 <i>বটটির সকল ফিচার ব্যবহার করতে আমাদের চ্যানেলে জয়েন করুন এবং 'ভেরিফাই জয়েন' বাটনে চাপুন।</i>\n\n"
                    "<code>[ স্ট্যাটাস: ভেরিফিকেশনের জন্য অপেক্ষায় ]</code>"
                )
            else:
                join_keyboard = ReplyKeyboardMarkup([
                    [KeyboardButton("📢 View Channel")],
                    [KeyboardButton("✅ Verify Join")]
                ], resize_keyboard=True)
                join_msg = (
                    f"{STYLISH_HEADER}"
                    "🚨 <b>[ ACCESS RESTRICTED ]</b> 🚨\n\n"
                    f"📌 <i>Official Channel Link: {REQUIRED_CHANNEL_LINK}</i>\n"
                    "📌 <i>Please subscribe to our channel first and click 'Verify Join' to unlock access.</i>\n\n"
                    "<code>[ STATUS: WAITING FOR VERIFICATION ]</code>"
                )
            
            await update.message.reply_text(join_msg, parse_mode="HTML", reply_markup=join_keyboard)
            return
    except Exception:
        pass

    if lang == 'bn':
        welcome_text = (
            f"{STYLISH_HEADER}"
            f"👤 <b>ব্যবহারকারী:</b> <code>{update.effective_user.first_name}</code>\n"
            f"🆔 <b>ইউজার আইডি:</b> <code>{user_id}</code>\n"
            f"⚡ <b>সিস্টেম স্ট্যাটাস:</b> <code>অনলাইন ও প্রস্তুত</code>\n"
            f"{DECO_DIVIDER}"
            "যেকোনো প্রশ্ন বা টেক্সট লিখে পাঠান। বট সেটি প্রসেস করে দ্রুত সঠিক উত্তর প্রদান করবে।\n"
            f"{DECO_DIVIDER}"
            "🔻 <b>নিচের বাটনগুলো ব্যবহার করুন:</b>"
        )
    else:
        welcome_text = (
            f"{STYLISH_HEADER}"
            f"👤 <b>User:</b> <code>{update.effective_user.first_name}</code>\n"
            f"🆔 <b>User ID:</b> <code>{user_id}</code>\n"
            f"⚡ <b>System Status:</b> <code>ONLINE & READY</code>\n"
            f"{DECO_DIVIDER}"
            "Send any prompt or message. The bot will automatically process and parse the optimal response.\n"
            f"{DECO_DIVIDER}"
            "🔻 <b>Use the options below:</b>"
        )

    await update.message.reply_text(welcome_text, parse_mode="HTML", reply_markup=get_main_keyboard(user_id))

async def handle_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = update.effective_user.id

    if not user_text:
        return

    if user_text == "🇧🇩 বাংলা (Bengali)":
        user_languages[user_id] = 'bn'
        await update.message.reply_text("✅ <b>ভাষা সফলভাবে 'বাংলা' সেট করা হয়েছে!</b>", parse_mode="HTML")
        await send_main_welcome(update, context, user_id)
        return

    elif user_text == "🇬🇧 English":
        user_languages[user_id] = 'en'
        await update.message.reply_text("✅ <b>Language successfully set to 'English'!</b>", parse_mode="HTML")
        await send_main_welcome(update, context, user_id)
        return

    elif user_text in ["🌐 ভাষা পরিবর্তন করুন", "🌐 Change Language"]:
        lang_text = (
            f"{STYLISH_HEADER}"
            "Please select your language / অনুগ্রহ করে আপনার ভাষা সিলেক্ট করুন:"
        )
        await update.message.reply_text(lang_text, parse_mode="HTML", reply_markup=get_language_keyboard())
        return

    lang = user_languages.get(user_id, 'bn')

    if user_text in ["🔮 রেফারেল dashboard", "🔮 Referral Dashboard"]:
        bot_username = (await context.bot.get_me()).username
        ref_link = f"https://t.me/{bot_username}?start={user_id}"
        count = referrals_db.get(user_id, 0)
        
        if lang == 'bn':
            ref_text = (
                "🚀 <b>[ রেফারেল ড্যাশবোর্ড ]</b> 🚀\n"
                f"{DECO_DIVIDER}"
                f"🔗 <b>আপনার লিংক:</b>\n<code>{ref_link}</code>\n\n"
                f"👥 <b>মোট রেফারেল:</b> <code>{count} জন</code>\n"
                f"🎁 <b>রিওয়ার্ড স্ট্যাটাস:</b> <code>সক্রিয়</code>\n"
                f"{DECO_DIVIDER}"
                "💡 <i>লিংকটি বন্ধুদের সাথে শেয়ার করুন!</i>"
            )
        else:
            ref_text = (
                "🚀 <b>[ REFERRAL DASHBOARD ]</b> 🚀\n"
                f"{DECO_DIVIDER}"
                f"🔗 <b>Your Link:</b>\n<code>{ref_link}</code>\n\n"
                f"👥 <b>Total Invited:</b> <code>{count}</code>\n"
                f"🎁 <b>Reward Status:</b> <code>ACTIVE</code>\n"
                f"{DECO_DIVIDER}"
                "💡 <i>Share this link to invite users and grow your network!</i>"
            )
        await update.message.reply_text(ref_text, parse_mode="HTML")
        return

    elif user_text in ["📊 বট পরিসংখ্যান", "📊 Bot Statistics"]:
        total_users = len(users_db)
        if lang == 'bn':
            status_text = (
                "📊 <b>[ সিস্টেম পরিসংখ্যান ]</b>\n"
                f"{DECO_DIVIDER}"
                f"👥 <b>মোট সক্রিয় ব্যবহারকারী:</b> <code>{total_users} জন</code>\n"
                f"⚡ <b>সার্ভার ইঞ্জিন:</b> <code>Python 3.x (Async)</code>\n"
                f"{DECO_DIVIDER}"
                "🟢 <i>বটের সকল সার্ভিস সক্রিয় রয়েছে।</i>"
            )
        else:
            status_text = (
                "📊 <b>[ LIVE BOT STATS ]</b>\n"
                f"{DECO_DIVIDER}"
                f"🌐 <b>Total Registered Users:</b> <code>{total_users}</code>\n"
                f"⚡ <b>Server Engine:</b> <code>Python 3.x (Async)</code>\n"
                f"{DECO_DIVIDER}"
                "🟢 <i>Bot state is fully optimized and active.</i>"
            )
        await update.message.reply_text(status_text, parse_mode="HTML")
        return

    elif user_text in ["💬 সাপোর্ট সাহায্য", "💬 Support & Help"]:
        if lang == 'bn':
            support_text = (
                "💬 <b>[ সাপোর্ট ও সাহায্য ]</b>\n"
                f"{DECO_DIVIDER}"
                "যেকোনো প্রয়োজনে সরাসরি অ্যাডমিনের সাথে যোগাযোগ করুন:\n\n"
                f"👨‍💻 <b>অ্যাডমিন কন্টাক্ট লিংক:</b> tg://user?id={ADMIN_ID}\n"
                f"🆔 <b>অ্যাডমিন আইডি:</b> <code>{ADMIN_ID}</code>"
            )
        else:
            support_text = (
                "💬 <b>[ HELP & SUPPORT ]</b>\n"
                f"{DECO_DIVIDER}"
                "Need assistance or reporting a bug?\n"
                "Contact the admin directly:\n\n"
                f"👨‍💻 <b>Admin Contact Link:</b> tg://user?id={ADMIN_ID}\n"
                f"🆔 <b>Admin ID:</b> <code>{ADMIN_ID}</code>"
            )
        await update.message.reply_text(support_text, parse_mode="HTML")
        return

    elif user_text in ["📢 আমাদের চ্যানেল", "📢 Official Channel", "📢 চ্যানেল দেখুন", "📢 View Channel"]:
        msg = f"📢 <b>Our Official Channel Link / আমাদের চ্যানেল লিংক:</b>\n{REQUIRED_CHANNEL_LINK}"
        await update.message.reply_text(msg, parse_mode="HTML")
        return

    elif user_text in ["⚙️ এডমিন প্যানেল", "⚙️ Admin Panel"]:
        if user_id == ADMIN_ID:
            admin_msg = (
                "⚙️ <b>[ ADMIN CONTROL CENTER ]</b> ⚙️\n"
                f"{DECO_DIVIDER}"
                "📢 <b>Broadcast Console Command:</b>\n"
                "To send a styled announcement to all users, type:\n\n"
                "<code>/admin Your broadcast message text</code>\n"
                f"{DECO_DIVIDER}"
                "⚠️ <i>Supports HTML formatting tags.</i>"
            )
            await update.message.reply_text(admin_msg, parse_mode="HTML")
        return

    elif user_text in ["✅ ভেরিফাই জয়েন", "✅ Verify Join"]:
        try:
            member = await context.bot.get_chat_member(chat_id=REQUIRED_CHANNEL, user_id=user_id)
            if member.status in ['left', 'kicked']:
                fail_msg = (
                    "❌ <b>[ VERIFICATION FAILED ]</b>\n\n"
                    "⚠️ You haven't joined the channel yet! / আপনি এখনো চ্যানেলে জয়েন করেননি!\n"
                    f"🔗 Channel Link: {REQUIRED_CHANNEL_LINK}"
                )
                await update.message.reply_text(fail_msg, parse_mode="HTML")
            else:
                success_msg = (
                    "🎉 <b>[ VERIFICATION SUCCESSFUL / ভেরিফিকেশন সফল ]</b>\n\n"
                    "🔓 Access granted! / আপনার এক্সেস সক্রিয় করা হয়েছে।"
                )
                await update.message.reply_text(success_msg, parse_mode="HTML", reply_markup=get_main_keyboard(user_id))
        except Exception:
            await update.message.reply_text("✅ <b>Welcome!</b>", parse_mode="HTML", reply_markup=get_main_keyboard(user_id))
        return

    encoded_text = urllib.parse.quote(user_text)
    full_url = f"{API_BASE_URL}{encoded_text}"

    loading_text = "⏳ <b><code>উত্তর তৈরি করা হচ্ছে...</code></b>" if lang == 'bn' else "⏳ <b><code>Processing query via API engine...</code></b>"
    status_msg = await update.message.reply_text(loading_text, parse_mode="HTML")

    try:
        req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            raw_data = response.read().decode('utf-8')
            json_data = json.loads(raw_data)
            
            if "reply" in json_data and json_data["reply"]:
                full_reply = json_data["reply"]
                
                paragraphs = [p.strip() for p in re.split(r'\n\s*\n', full_reply) if p.strip()]
                
                if paragraphs:
                    best_reply = max(paragraphs, key=len)
                else:
                    best_reply = full_reply

                header_label = "[ উত্তর / RESPONSE ]" if lang == 'bn' else "[ API RESPONSE RESULT ]"
                footer_label = "⚡ সাফল্যজনকভাবে সম্পন্ন হয়েছে।" if lang == 'bn' else "⚡ Processed successfully."

                styled_output = (
                    f"✨ <b>{header_label}</b> ✨\n"
                    f"{DECO_DIVIDER}"
                    f"{best_reply}\n"
                    f"{DECO_DIVIDER}"
                    f"<i>{footer_label}</i>"
                )
                await status_msg.edit_text(styled_output, parse_mode="HTML")
            else:
                err_text = "❌ <b>[ কোনো উত্তর পাওয়া যায়নি ]</b>" if lang == 'bn' else "❌ <b>[ NO RESPONSE RETURNED ]</b>"
                await status_msg.edit_text(err_text, parse_mode="HTML")

    except Exception as e:
        await status_msg.edit_text(
            f"❌ <b>[ API ERROR ]</b>\n<code>{str(e)}</code>", 
            parse_mode="HTML"
        )

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
        "📢 <b>[ GLOBAL ANNOUNCEMENT / গ্লোবাল নোটিশ ]</b> 📢\n"
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
        "✅ <b>[ BROADCAST COMPLETED ]</b>\n\n"
        f"🎯 <b>Delivered:</b> <code>{success}</code>\n"
        f"❌ <b>Failed:</b> <code>{failed}</code>",
        parse_mode="HTML"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all_messages))

    print("\n[+] Bot Engine Online and Listening...")
    app.run_polling()

if __name__ == "__main__":
    main()
