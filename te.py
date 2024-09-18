from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import subprocess
import json
import os
import logging

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

# Configuration
MINER_PATH = ""
WALLET_ADDRESS = "4385pTGhmZUK5ZcAqekKXk8Z3UuSxezEUYmhA9j9Ckmy5eTFatTEFaJJnxgQCg48ef3opVwsFfhhX17FTCA2hM6UT17Rn9x"
BOT_TOKEN = "7435606545:AAGLUaOZ0ZlEekkRgCXPCbL9chmmVUSMppM"
MINING_POOL = "rtm.suprnova.cc:4273"
PAYMENT_HISTORY_FILE = "payment_history.json"

# Payment history initialization
if not os.path.isfile(PAYMENT_HISTORY_FILE):
    with open(PAYMENT_HISTORY_FILE, "w") as f:
        json.dump([], f)

async def start_mining(update: Update, context: CallbackContext):
    """মাইনিং শুরু করো।"""
    logger.info('মাইনিং প্রক্রিয়া শুরু হচ্ছে...')
    command = [
        MINER_PATH, 
        "-a", "gr",
        "-o", MINING_POOL,
        "--tls",
        "-u", WALLET_ADDRESS,
        "-p", "x"
    ]
    
    try:
        # মাইনিং প্রক্রিয়া শুরু করার চেষ্টা
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        context.chat_data['process'] = process
        await update.message.reply_text('Monero মাইনিং শুরু হয়েছে!')
        logger.info('মাইনিং প্রক্রিয়া সফলভাবে শুরু হয়েছে।')
        
        # ঐচ্ছিক: মাইনিং প্রক্রিয়ার আউটপুট পর্যবেক্ষণ
        stdout, stderr = process.communicate(timeout=10)
        if stdout:
            logger.info(f"মাইনিং আউটপুট: {stdout.decode()}")
        if stderr:
            logger.error(f"মাইনিং ত্রুটি: {stderr.decode()}")
            await update.message.reply_text(f"মাইনিং ত্রুটি: {stderr.decode()}")
    
    except Exception as e:
        logger.error(f"মাইনিং শুরু করতে ব্যর্থ: {e}")
        await update.message.reply_text(f"মাইনিং শুরু করতে ব্যর্থ: {str(e)}")

async def stop_mining(update: Update, context: CallbackContext):
    """মাইনিং বন্ধ করো।"""
    process = context.chat_data.get('process')
    if process:
        process.terminate()
        await update.message.reply_text('Monero মাইনিং বন্ধ করা হয়েছে!')
        logger.info('মাইনিং প্রক্রিয়া বন্ধ করা হয়েছে।')
    else:
        await update.message.reply_text('মাইনিং প্রক্রিয়া পাওয়া যায়নি।')
        logger.warning('মাইনিং প্রক্রিয়া বন্ধ করার চেষ্টা করা হয়েছে, কিন্তু কোনো প্রক্রিয়া পাওয়া যায়নি।')

def main():
    """বট চালানোর মূল ফাংশন।"""
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start_mining", start_mining))
    application.add_handler(CommandHandler("stop_mining", stop_mining))
    
    application.run_polling()

if __name__ == '__main__':
    main()
