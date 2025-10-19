from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.utils.helpers import get_client_type_keyboard

class RegistrationStates(StatesGroup):
    waiting_for_role = State()
    waiting_for_vehicle_details = State()
    waiting_for_id_photo = State()
    waiting_for_client_details = State()

async def process_role(message: types.Message, state: FSMContext):
    role = message.text
    if role == "Mensajero":
        await state.update_data(role=role)
        await message.answer("Por favor, proporciona detalles sobre tu vehículo (marca, modelo, placa):")
        await RegistrationStates.waiting_for_vehicle_details.set()
    elif role == "Cliente":
        await state.update_data(role=role)
        await message.answer("¿Eres una empresa o un particular?", reply_markup=get_client_type_keyboard())
        await RegistrationStates.waiting_for_client_details.set()
    else:
        await message.answer("Por favor, elige una opción válida: Mensajero o Cliente.")

async def process_vehicle_details(message: types.Message, state: FSMContext):
    vehicle_details = message.text
    await state.update_data(vehicle_details=vehicle_details)
    await message.answer("Por favor, envía una fotografía tuya sosteniendo tu cédula de identidad.")
    await RegistrationStates.waiting_for_id_photo.set()

async def process_client_details(message: types.Message, state: FSMContext):
    client_type = message.text
    if client_type in ["Empresa", "Particular"]:
        await state.update_data(client_type=client_type)
        await message.answer("Por favor, envía una fotografía tuya sosteniendo tu cédula de identidad.")
        await RegistrationStates.waiting_for_id_photo.set()
    else:
        await message.answer("Por favor, elige una opción válida: Empresa o Particular.")

async def process_id_photo(message: types.Message, state: FSMContext, bot: Bot):
    photo = message.photo[-1].file_id
    user_data = await state.get_data()
    role = user_data.get('role')
    vehicle_details = user_data.get('vehicle_details', '')
    client_type = user_data.get('client_type', '')
    
    # Send the information to the admin for verification
    admin_chat_id = bot.get_current().get('config').admin_chat_id
    caption = f"Nuevo registro:\nRol: {role}\n"
    if role == "Mensajero":
        caption += f"Detalles del vehículo: {vehicle_details}\n"
    elif role == "Cliente":
        caption += f"Tipo de cliente: {client_type}\n"
    caption += f"Usuario: {message.from_user.id}"
    await bot.send_photo(admin_chat_id, photo, caption=caption)
    await message.answer("Tu información ha sido enviada al administrador para verificación. Te notificaremos una vez que sea revisada.")
    await state.finish()

def register_handlers(dp):
    dp.register_message_handler(process_role, state=RegistrationStates.waiting_for_role)
    dp.register_message_handler(process_vehicle_details, state=RegistrationStates.waiting_for_vehicle_details)
    dp.register_message_handler(process_client_details, state=RegistrationStates.waiting_for_client_details)
    dp.register_message_handler(process_id_photo, content_types=['photo'], state=RegistrationStates.waiting_for_id_photo)