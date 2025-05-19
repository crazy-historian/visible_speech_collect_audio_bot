# keyboards/reply.py
from aiogram import types

def start_keyboard():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="📝 Заполнить анкету"), types.KeyboardButton(text="❌ Отмена")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )

def gender_keyboard():
    return types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text="Мужской"), types.KeyboardButton(text="Женский")]],
        resize_keyboard=True
    )

def hearing_issue_keyboard():
    return types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text="Да"), types.KeyboardButton(text="Нет")]],
        resize_keyboard=True
    )

def hearing_degree_keyboard():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Легкая"), types.KeyboardButton(text="Умеренная")],
            [types.KeyboardButton(text="Тяжелая"), types.KeyboardButton(text="Глухота")]
        ],
        resize_keyboard=True
    )

def consent_keyboard():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="✅ Да")],
            [types.KeyboardButton(text="❌ Нет")]
        ],
        resize_keyboard=True
    )

def assignment_keyboard():
    return types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text="📩 Получить задание")]],
        resize_keyboard=True
    )