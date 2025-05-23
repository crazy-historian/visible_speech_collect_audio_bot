import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
API_TOKEN = os.getenv('TG_BOT_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# Определяем состояния анкеты
class Form(StatesGroup):
    age = State()
    gender = State()
    hearing_issue = State()
    hearing_degree = State()
    consent = State()
    assignment = State()
    audio = State()
    


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="📝 Заполнить анкету"),
                types.KeyboardButton(text="❌ Отмена")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберете действие"
    )
    await message.answer(
        "Добро пожаловать! Этот бот собирает аудиоданные для лингвистического исследования.\n"
        "Выберите действие:",
        reply_markup=keyboard
    )

# Хэндлер на команду /cancel и кнопку "Отмена"
@dp.message(Command("cancel"))
@dp.message(F.text == "❌ Отмена")
async def cancel_handler(message: types.Message,  state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()

    await message.answer(
        "Действие отменено",
        reply_markup=types.ReplyKeyboardRemove()
    )

# Хэндлер для кнопки "Заполнить анкету"
@dp.message(F.text == "📝 Заполнить анкету")
async def start_questionnaire(message: types.Message, state: FSMContext):
    await state.set_state(Form.age)
    await message.answer("Сколько вам полных лет?", reply_markup=types.ReplyKeyboardRemove())

# Обработчик возраста
@dp.message(Form.age)
async def process_age(message: types.Message, state: FSMContext):

    try:
        print(f'введен возраст: {message.text}, int это {int(message.text)}')
        age = int(message.text)
        if age < 1 or age > 120:
            raise ValueError
        await state.update_data(age=age)
      
        await state.set_state(Form.gender)
        
        gender_keyboard = types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="Мужской"), 
                 types.KeyboardButton(text="Женский")],
            ],
            resize_keyboard=True
        )
        await message.answer("Укажите ваш пол:", reply_markup=gender_keyboard)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный возраст (число от 1 до 120)!")

# Обработчик пола
@dp.message(Form.gender)
async def process_gender(message: types.Message, state: FSMContext):
    if message.text not in ["Мужской", "Женский"]:
        await message.answer("Пожалуйста, используйте кнопки для выбора!")
        return
    
    await state.update_data(gender=message.text)
    await state.set_state(Form.hearing_issue)
    
    hearing_keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Да"), 
             types.KeyboardButton(text="Нет")],
        ],
        resize_keyboard=True
    )
    await message.answer("Есть ли у вас нарушения слуха?", reply_markup=hearing_keyboard)

# Обработчик нарушения слуха
@dp.message(Form.hearing_issue)
async def process_hearing_issue(message: types.Message, state: FSMContext):
    if message.text not in ["Да", "Нет"]:
        await message.answer("Пожалуйста, используйте кнопки для ответа!")
        return
    
    if message.text == "Нет":
        await state.update_data(hearing_issue=False)
        await finish_questionnaire(message, state)
    else:
        await state.update_data(hearing_issue=True)
        await state.set_state(Form.hearing_degree)
        
        degree_keyboard = types.ReplyKeyboardMarkup(
            keyboard=[
                [types.KeyboardButton(text="Легкая"), types.KeyboardButton(text="Умеренная")],
                [types.KeyboardButton(text="Тяжелая"), types.KeyboardButton(text="Глухота")],
            ],
            resize_keyboard=True
        )
        await message.answer("Укажите степень нарушения:", reply_markup=degree_keyboard)

# Обработчик степени нарушения
@dp.message(Form.hearing_degree)
async def process_hearing_degree(message: types.Message, state: FSMContext):
    valid_degrees = ["Легкая", "Умеренная", "Тяжелая", "Глухота"]
    if message.text not in valid_degrees:
        await message.answer("Пожалуйста, выберите вариант из списка!")
        return
    
    await state.update_data(hearing_degree=message.text)
    await finish_questionnaire(message, state)

async def finish_questionnaire(message: types.Message, state: FSMContext):
    data = await state.get_data()
    
    response = (
        "Спасибо за анкету! Ваши данные:\n"
        f"Возраст: {data['age']}\n"
        f"Пол: {data['gender']}\n"
        f"Нарушения слуха: {'Да' if data['hearing_issue'] else 'Нет'}"
    )
    
    if data.get('hearing_degree'):
        response += f"\nСтепень нарушения: {data['hearing_degree']}"
    
    await message.answer(response)
    
    # Переходим к этапу согласия
    await state.set_state(Form.consent)
    
    # Формируем текст согласия в зависимости от возраста
    age = data.get('age', 0)
    if age < 18:
        consent_text = "⚠️ Для участия необходимо согласие родителя/опекуна!\nПожалуйста, подтвердите согласие:"
    else:
        consent_text = "🔒 Пожалуйста, подтвердите ваше согласие на обработку персональных данных:"
    
    # Создаем клавиатуру для согласия
    consent_keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="✅ Даю согласие")],
            [types.KeyboardButton(text="❌ Отказаться")]
        ],
        resize_keyboard=True
    )
    
    await message.answer(consent_text, reply_markup=consent_keyboard)

# Обработчик согласия
@dp.message(Form.consent)
async def process_consent(message: types.Message, state: FSMContext):
    if message.text not in ["✅ Даю согласие", "❌ Отказаться"]:
        await message.answer("Пожалуйста, используйте кнопки для ответа!")
        return
    
    data = await state.get_data()
    print(data)
    
    if message.text == "✅ Даю согласие":
        await state.set_state(Form.assignment)
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=[[types.KeyboardButton(text="📩 Получить задание")]],
            resize_keyboard=True
        )
        await message.answer(
            "🎉 Отлично! Хотите получить текст для записи?",
            reply_markup=keyboard
        )
        
        # Для несовершеннолетних
        if data['age'] < 18:
            await message.answer("📞 Мы свяжемся с вашим законным представителем для подтверждения.")
            
    else:
        await message.answer("❌ Согласие не получено. Все данные будут удалены.", reply_markup=types.ReplyKeyboardRemove())
        await state.clear()

# Обработчик получения задания
@dp.message(Form.assignment)
@dp.message(F.text == "📩 Получить задание")
async def send_assignment(message: types.Message, state: FSMContext):
    # Текст для чтения (можно вынести в отдельный файл)
    assignment_text = (
        "Пожалуйста, прочитайте вслух следующий текст:\n\n"
        "«Наука - это организованное знание. "
        "Мудрость - это организованная жизнь.»\n\n"
        "Сделайте запись голосовым сообщением."
    )
    
    await message.answer(
        assignment_text,
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(Form.audio)  # Переходим в состояние ожидания аудио

# Новый обработчик для аудио сообщений
@dp.message(Form.audio, F.voice)
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
@dp.message(Form.audio)
async def handle_wrong_content(message: types.Message):
    # Удаляем предыдущую клавиатуру
    await message.answer(
        "⚠️ Пожалуйста, отправьте именно голосовое сообщение!\n"
        "Используйте иконку микрофона в приложении.",
        reply_markup=types.ReplyKeyboardRemove()
)

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())