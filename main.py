# main.py
from aiogram import Bot, Dispatcher
from config.config import API_TOKEN
from handlers import start, questionnaire, task, consent, voice_message#, assignment, errors
from utils.logging import setup_logging

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


dp.include_router(start.router)
dp.include_router(questionnaire.router)
dp.include_router(consent.router)
dp.include_router(task.router)
dp.include_router(voice_message.router)

# Добавь остальные роутеры (consent, assignment, errors) по мере их создания

async def main():
    setup_logging()
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())