import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import my_router

from config import TOKEN
import logging

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router=my_router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот завершен')
