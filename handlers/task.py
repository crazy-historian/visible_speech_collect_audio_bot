# handlers/task.py
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from states.form import Form
from aiogram import F
from aiogram.enums import ParseMode

router = Router()

def load_task_text():
    with open('texts/poem.md', 'r', encoding='utf-8') as file:
        raw_text = file.read()
    return raw_text


@router.message(Form.task)
@router.message(F.text == "📩 Получить задание")
async def send_task(message: types.Message, state: FSMContext):
    
    task = load_task_text()
    await message.answer(
        "Пришлите аудиосообщение, где Вы зачитываете следующее стихотворение:",
        reply_markup=types.ReplyKeyboardRemove()
    )
    print(task)
    await message.answer(
        task,
        parse_mode=ParseMode.MARKDOWN_V2  # Добавляем парсинг Markdown
    )
    await state.set_state(Form.audio)  # Переходим к ожиданию аудио