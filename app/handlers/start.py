from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.utils.helpers import get_role_keyboard

class RegistrationStates(StatesGroup):
    waiting_for_role = State()

async def start(message: types.Message):
    await message.answer("Bienvenido al bot de Mandadero. ¿Eres un mensajero o un cliente?", reply_markup=get_role_keyboard())
    await RegistrationStates.waiting_for_role.set()

def register_handlers(dp):
    dp.register_message_handler(start, Command("start"))