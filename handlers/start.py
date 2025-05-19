# handlers/start.py
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.reply import start_keyboard
from aiogram import F

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Добро пожаловать! Этот бот собирает аудиоданные для лингвистического исследования.\n"
        "Выберите действие:",
        reply_markup=start_keyboard()
    )

@router.message(Command("cancel"))
@router.message(F.text == "❌ Отмена")
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())