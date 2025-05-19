# states/form.py
from aiogram.fsm.state import StatesGroup, State

class Form(StatesGroup):
    age = State()
    gender = State()
    hearing_issue = State()
    hearing_degree = State()
    consent = State()
    assignment = State()
    audio = State()
    task = State()
    audio_message = State()