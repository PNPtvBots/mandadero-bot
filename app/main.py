import logging
from aiogram import Bot, Dispatcher, executor
from app.config import Config
from app.handlers import start, registration, admin
from app.services.database import init_db

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize config
config = Config()

# Initialize bot and dispatcher
bot = Bot(token=config.bot_token)
dp = Dispatcher(bot)

# Register handlers
start.register_handlers(dp)
registration.register_handlers(dp)
admin.register_handlers(dp)

async def on_startup(dispatcher):
    await init_db(config.db_url)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)