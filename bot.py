import os
import telebot

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8587244331"))

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: message.from_user.id != ADMIN_ID)
def receive_from_user(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name or "غير محدد"
    username = f"@{message.from_user.username}" if message.from_user.username else "لا يوجد"
    text = message.text or message.caption or "[ملف أو وسائط بدون نص]"
    
    details = (
        f"📩 **تفاصيل الرسالة الجديدة:**\n"
        f"👤 الاسم: {first_name}\n"
        f"🔗 اليوزرنيم: {username}\n"
        f"🆔 المعرف: `{user_id}`\n\n"
        f"💬 المحتوى:\n{text}"
    )
    
    bot.send_message(ADMIN_ID, details, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID and message.reply_to_message is not None)
def send_to_user(message):
    replied_text = message.reply_to_message.text
    
    try:
        if "🆔 المعرف:" in replied_text:
            lines = replied_text.split("\n")
            for line in lines:
                if "🆔 المعرف:" in line:
                    target_user_id = int(line.split("`")[1])
                    bot.send_message(target_user_id, message.text)
                    bot.reply_to(message, "✅ تم إرسال الرد بنجاح.")
                    return
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ في إرسال الرد: {e}")

bot.infinity_polling(timeout=60, long_polling_timeout=60)
