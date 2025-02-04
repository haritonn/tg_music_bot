from aiogram import Dispatcher, Bot, html
from aiogram.enums import ParseMode
from aiogram.dispatcher.dispatcher import MemoryStorage
from aiogram.client.bot import DefaultBotProperties

import logging
import asyncio
import sys 
import os 

from dotenv import load_dotenv
from app.handlers import router

load_dotenv('stuff.env')
TOKEN = os.getenv('TOKEN')

dp = Dispatcher(storage = MemoryStorage())

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    dp.include_router(router)
    logging.basicConfig(level = "INFO", stream = sys.stdout)
    asyncio.run(main())