# handlers/errors.py
from aiogram import Router
from aiogram.types import ErrorEvent
import logging

router = Router()

@router.errors()
async def error_handler(event: ErrorEvent):
    logging.error(f"Произошла ошибка: {event.exception}")
    await event.update.message.answer("Что-то пошло не так. Попробуйте позже.")