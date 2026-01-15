import asyncio
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime
from collections import defaultdict
from typing import Dict, Optional, List
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.methods import DeleteWebhook
from aiogram.types import Message, WebAppInfo, CallbackQuery
from aiogram.enums import ParseMode
from dotenv import load_dotenv
import sys
import time

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEBAPP_URL = os.getenv('WEBAPP_URL') 
ERROR_LOG_CHAT_ID = os.getenv("ERROR_LOG_CHAT_ID")

if not TOKEN:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN variable")

# Rate limiting storage
user_last_request: Dict[int, float] = {}
RATE_LIMIT_SECONDS = 1  # 1 second between requests per user


TEXTS = {
    'en': {
        'welcome_message': '''Welcome to Our Store!

Discover amazing products and exclusive deals.

✨ Tap the button below to explore our collection!''',
        'view_store': '🛍️ Open Store',
        'want_same': '💬 Contact Us',
        'join_channel': '📢 Join Channel',
        'error_message': '⚠️ Something went wrong. Please try again.',
        'rate_limit': '⏱️ Please wait a moment before trying again.',
        'payment_success': '✅ Payment successful!',
        'confetti_message': '🎊 Welcome! Enjoy your shopping experience! 🎉',
        'store_info': '🏪 <b>Our Store</b>\n\nBrowse our amazing products!\n\nUse the buttons below to navigate.',
        'opening_store': '🛍️ Opening store...'
    },
    'ru': {
        'welcome_message': '''Добро пожаловать в наш магазин!

Откройте для себя удивительные товары и эксклюзивные предложения.

✨ Нажмите кнопку ниже, чтобы изучить нашу коллекцию!''',
        'view_store': '🛍️ Открыть магазин',
        'want_same': '💬 Связаться с нами',
        'join_channel': '📢 Присоединиться к каналу',
        'error_message': '⚠️ Что-то пошло не так. Пожалуйста, попробуйте еще раз.',
        'rate_limit': '⏱️ Пожалуйста, подождите немного перед повторной попыткой.',
        'payment_success': '✅ Платеж успешен!',
        'confetti_message': '🎊 Добро пожаловать! Наслаждайтесь покупками! 🎉',
        'store_info': '🏪 <b>Наш магазин</b>\n\nПросматривайте наши удивительные товары!\n\nИспользуйте кнопки ниже для навигации.',
        'opening_store': '🛍️ Открываем магазин...'
    },
    'hi': {
        'welcome_message': '''हमारे स्टोर में आपका स्वागत है!

अद्भुत उत्पादों और विशेष ऑफर्स की खोज करें।

✨ हमारे कलेक्शन को देखने के लिए नीचे दिए गए बटन पर टैप करें!''',
        'view_store': '🛍️ स्टोर खोलें',
        'want_same': '💬 हमसे संपर्क करें',
        'join_channel': '📢 चैनल से जुड़ें',
        'error_message': '⚠️ कुछ गलत हुआ। कृपया फिर से कोशिश करें।',
        'rate_limit': '⏱️ कृपया फिर से कोशिश करने से पहले थोड़ा इंतजार करें।',
        'payment_success': '✅ भुगतान सफल!',
        'confetti_message': '🎊 स्वागत है! अपने शॉपिंग अनुभव का आनंद लें! 🎉',
        'store_info': '🏪 <b>हमारा स्टोर</b>\n\nहमारे अद्भुत उत्पादों को देखें!\n\nनेविगेट करने के लिए नीचे दिए गए बटन का उपयोग करें।',
        'opening_store': '🛍️ स्टोर खोल रहे हैं...'
    }
}

def get_user_language(language_code: str) -> str:
    """Get user language, default to English if not supported."""
    supported_languages = ['ru', 'hi']
    return language_code if language_code in supported_languages else 'en'

def get_text(language_code: str, key: str) -> str:
    """Get localized text for user language."""
    lang = get_user_language(language_code)
    return TEXTS[lang].get(key, TEXTS['en'][key])

# Message effect IDs
EFFECTS = {
    'confetti': '5046509860389126442',  # 🎉 Confetti
    'fire': '5104841245755180586',      # 🔥 Fire
    'heart': '5159385139981059251',     # ❤️ Heart
    #see more in messageAnimatedEffectIds.md file
}

def sanitize_input(text: str, max_length: int = 4096) -> str:
    """Sanitize user input to prevent injection attacks."""
    if not text:
        return ""
    # Remove control characters
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
    # Truncate to max length
    return text[:max_length].strip()

def check_rate_limit(user_id: int) -> bool:
    """Check if user is rate limited."""
    current_time = time.time()
    last_request = user_last_request.get(user_id, 0)
    
    if current_time - last_request < RATE_LIMIT_SECONDS:
        return False
    
    user_last_request[user_id] = current_time
    return True

def setup_logging():
    os.makedirs("logs", exist_ok=True)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    file_handler = TimedRotatingFileHandler(
        filename='logs/bot.log',
        when='midnight',
        interval=1,
        backupCount=7,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    logging.basicConfig(
        level=logging.INFO,
        handlers=[console_handler, file_handler],
        force=True
    )

bot = Bot(TOKEN)
dp = Dispatcher()

setup_logging()

@dp.message(CommandStart())
async def start_command(message: Message):
    """Handle /start command with confetti effect and webapp link."""
    try:
        user_id = message.from_user.id
        user_name = sanitize_input(message.from_user.first_name or "User")
        user_lang = message.from_user.language_code or 'en'
        
        # Rate limiting
        if not check_rate_limit(user_id):
            await message.answer(get_text(user_lang, 'rate_limit'))
            return
        
        # Create keyboard with webapp and regular buttons
        keyboard_buttons = []
        
        # Webapp button (if URL is configured)
        if WEBAPP_URL:
            keyboard_buttons.append([
                types.InlineKeyboardButton(
                    text=get_text(user_lang, 'view_store'),
                    web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ])
        
        # Regular URL buttons
        keyboard_buttons.extend([
            [types.InlineKeyboardButton(
                text=get_text(user_lang, 'want_same'), 
                url="https://t.me/your_support_bot"
            )],
            [types.InlineKeyboardButton(
                text=get_text(user_lang, 'join_channel'),
                url="https://t.me/your_channel"
            )]
        ])
        
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
        
        # Send welcome message with confetti effect
        welcome_text = get_text(user_lang, 'welcome_message')
        await message.answer(
            welcome_text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML,
            message_effect_id=EFFECTS['confetti']  # 🎉 Confetti effect
        )
        
        logging.info(
            f"User {sanitize_input(message.from_user.username or 'N/A')} "
            f"({user_id}) started the bot with language: {user_lang}"
        )
            
    except Exception as e:
        logging.error(f"Error in start_command: {str(e)}", exc_info=True)
        user_lang = message.from_user.language_code or 'en'
        await message.answer(get_text(user_lang, 'error_message'))
        
        # Send error notification to admin
        if ERROR_LOG_CHAT_ID:
            try:
                await bot.send_message(
                    ERROR_LOG_CHAT_ID,
                    f"⚠️ Error in start_command:\n{str(e)[:500]}"
                )
            except:
                pass

@dp.callback_query(F.data == "order")
async def handle_order_callback(callback: CallbackQuery):
    """Handle order callback with validation."""
    try:
        user_id = callback.from_user.id
        user_lang = callback.from_user.language_code or 'en'
        
        # Rate limiting
        if not check_rate_limit(user_id):
            await callback.answer(get_text(user_lang, 'rate_limit'), show_alert=True)
            return
        
        # Validate callback ownership (security check)
        if callback.message and callback.message.chat.id != user_id:
            await callback.answer("⛔ Unauthorized action", show_alert=True)
            logging.warning(
                f"SECURITY: Unauthorized callback attempt by user {user_id}"
            )
            return
        
        await callback.answer(get_text(user_lang, 'opening_store'), show_alert=False)
        
        # Send store information
        await callback.message.answer(
            get_text(user_lang, 'store_info'),
            parse_mode=ParseMode.HTML,
            message_effect_id=EFFECTS['fire']
        )
        
        logging.info(f"User {user_id} opened store via callback with language: {user_lang}")
        
    except Exception as e:
        logging.error(f"Error in handle_order_callback: {str(e)}", exc_info=True)
        user_lang = callback.from_user.language_code or 'en'
        await callback.answer(get_text(user_lang, 'error_message'), show_alert=True)

async def main():
    try:
        print("Starting the bot...")
        await bot(DeleteWebhook(drop_pending_updates=True))
        
        logging.info("Bot started successfully")
        print("Bot started successfully!")
        
        print("Starting polling...")
        await dp.start_polling(bot)
        
    except Exception as e:
        logging.error(f"Error in main: {str(e)}", exc_info=True)
        print(f"FATAL ERROR in main: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
        print("Bot stopped by user")
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}", exc_info=True)
        print(f"FATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()