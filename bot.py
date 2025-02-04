from aiogram import Dispatcher, Bot, html
from aiogram.types import BotCommand
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
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

async def on_startup(bot: Bot) -> None:
    """Building startup command /start"""
    commands = [BotCommand(command = 'start', description = 'Launch bot'), BotCommand(command = 'credits', description = 'tg/source code'),
                BotCommand(command = 'name', description = 'search song by name'), BotCommand(command = 'link', description = 'search song by link')]
    await bot.set_my_commands(commands)

dp.startup.register(on_startup)

async def main() -> None:
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    dp.include_router(router)
    logging.basicConfig(level = "INFO", stream = sys.stdout)
    asyncio.run(main())