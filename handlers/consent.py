# handlers/consent.py
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from states.form import Form
from keyboards.reply import assignment_keyboard

router = Router()

@router.message(Form.consent)
async def process_consent(message: types.Message, state: FSMContext):
    if message.text == "✅ Да":
        await state.set_state(Form.task)  # Переходим в состояние задания
        await message.answer("Спасибо!", reply_markup=assignment_keyboard())
        
    else:
        await message.answer("Согласие не получено. Все ваши данные будут удалены.")
        await state.clear()