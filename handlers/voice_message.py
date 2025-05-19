# handlers/consent.py
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from states.form import Form
from keyboards.reply import assignment_keyboard
from aiogram import F


router = Router()

@router.message(Form.audio, F.voice)
async def process_audio(message: types.Message, state: FSMContext):
    voice = message.voice
    duration = voice.duration  # Получаем длительность аудио
    
    # Mock-обработка: просто показываем информацию
    await message.answer(
        f"✅ Аудио получено!\n"
        f"Длительность: {duration} секунд\n"
        f"Формат: .ogg\n"
        f"Размер: {voice.file_size // 1024} КБ"
    )
    
    # Здесь будет логика сохранения аудио
    await state.clear()

# Обработчик для ЛЮБЫХ других сообщений в состоянии audio
@router.message(Form.audio)
async def handle_wrong_content(message: types.Message):
    # Удаляем предыдущую клавиатуру
    await message.answer(
        "⚠️ Пожалуйста, отправьте именно голосовое сообщение!\n"
        "Используйте иконку микрофона в приложении.",
        reply_markup=types.ReplyKeyboardRemove()
)