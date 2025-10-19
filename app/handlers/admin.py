from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from app.services.verification import notify_user

async def approve_registration(message: types.Message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.answer("Por favor, responde a un mensaje de registro para aprobar.")
        return
    
    user_id = message.reply_to_message.caption.split("Usuario: ")[-1]
    await notify_user(int(user_id), 'approved', message.bot)
    await message.answer(f"Registro del usuario {user_id} aprobado.")

async def reject_registration(message: types.Message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.answer("Por favor, responde a un mensaje de registro para rechazar.")
        return
    
    user_id = message.reply_to_message.caption.split("Usuario: ")[-1]
    await notify_user(int(user_id), 'rejected', message.bot)
    await message.answer(f"Registro del usuario {user_id} rechazado.")

def register_handlers(dp):
    dp.register_message_handler(approve_registration, Command("approve"))
    dp.register_message_handler(reject_registration, Command("reject"))