# handlers/questionnaire.py
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram import F
from states.form import Form
from keyboards.reply import gender_keyboard, hearing_issue_keyboard, hearing_degree_keyboard, consent_keyboard
from utils.markdown import escape_markdown_v2


router = Router()

# Обработчик для начала анкеты
@router.message(F.text =="📝 Заполнить анкету")
async def start_questionnaire(message: types.Message, state: FSMContext):
    """Запускает анкету, начиная с вопроса о возрасте."""
    await state.set_state(Form.age)
    await message.answer("Сколько вам полных лет?", reply_markup=types.ReplyKeyboardRemove())

# Обработчик возраста
@router.message(Form.age)
async def process_age(message: types.Message, state: FSMContext):
    """Обрабатывает введенный возраст и переходит к вопросу о поле."""
    try:
        age = int(message.text)
        if age < 1 or age > 120:  # Устанавливаем разумный диапазон возраста
            raise ValueError
        await state.update_data(age=age)
        await state.set_state(Form.gender)
        await message.answer("Укажите ваш пол:", reply_markup=gender_keyboard())
    except ValueError:
        await message.answer("Пожалуйста, введите корректный возраст (число от 1 до 120)!")

# Обработчик пола
@router.message(Form.gender)
async def process_gender(message: types.Message, state: FSMContext):
    """Обрабатывает выбор пола и переходит к вопросу о нарушениях слуха."""
    if message.text not in ["Мужской", "Женский"]:
        await message.answer("Пожалуйста, используйте кнопки для выбора!")
        return
    
    await state.update_data(gender=message.text)
    await state.set_state(Form.hearing_issue)
    await message.answer("Есть ли у вас нарушения слуха?", reply_markup=hearing_issue_keyboard())

# Обработчик вопроса о нарушениях слуха
@router.message(Form.hearing_issue)
async def process_hearing_issue(message: types.Message, state: FSMContext):
    """Обрабатывает ответ о наличии нарушений слуха."""
    if message.text not in ["Да", "Нет"]:
        await message.answer("Пожалуйста, используйте кнопки для ответа!")
        return
    
    if message.text == "Нет":
        await state.update_data(hearing_issue=False)
        await finish_questionnaire(message, state)
    else:
        await state.update_data(hearing_issue=True)
        await state.set_state(Form.hearing_degree)
        await message.answer("Укажите степень нарушения:", reply_markup=hearing_degree_keyboard())

# Обработчик степени нарушения слуха
@router.message(Form.hearing_degree)
async def process_hearing_degree(message: types.Message, state: FSMContext):
    """Обрабатывает выбор степени нарушения и завершает анкету."""
    valid_degrees = ["Легкая", "Умеренная", "Тяжелая", "Глухота"]
    if message.text not in valid_degrees:
        await message.answer("Пожалуйста, выберите вариант из списка!")
        return
    
    await state.update_data(hearing_degree=message.text)
    await finish_questionnaire(message, state)

# Функция завершения анкеты
async def finish_questionnaire(message: types.Message, state: FSMContext):
    """Выводит собранные данные и переводит бота в состояние согласия."""
    
    response = ("Спасибо за анкету!")
    
    await message.answer(response)
    
    # Переход к этапу согласия
    await state.set_state(Form.consent)

    with open('texts/agreement.md', 'r', encoding='utf-8') as file:
        agreement_text = file.read()
        agreement_text = escape_markdown_v2(agreement_text)
        await message.answer(agreement_text, reply_markup=consent_keyboard(), parse_mode='MarkdownV2')