from aiogram import types
from aiogram.dispatcher import FSMContext
from config.settings import dp
from utils.keyboards import main_keyboard

@dp.message_handler(commands=['help', 'start'], state='*')
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "Добро пожаловать! Этот бот собирает аудиоданные для лингвистического исследования.\n"
        "Начните с команды /start для заполнения анкеты.",
        reply_markup=main_keyboard()
    )

@dp.message_handler(commands='cancel', state='*')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.answer(
        "Действие отменено. Вы можете начать заново с /start",
        reply_markup=types.ReplyKeyboardRemove()
    )