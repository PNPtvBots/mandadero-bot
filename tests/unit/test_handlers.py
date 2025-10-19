import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram import types
from app.handlers.start import start
from app.handlers.registration import process_role, process_vehicle_details, process_client_details, process_id_photo
from app.handlers.admin import approve_registration, reject_registration

@pytest.mark.asyncio
async def test_start_handler():
    message = AsyncMock(spec=types.Message)
    message.answer = AsyncMock()
    await start(message)
    message.answer.assert_called_once_with(
        "Bienvenido al bot de Mandadero. ¿Eres un mensajero o un cliente?",
        reply_markup=MagicMock()
    )

@pytest.mark.asyncio
async def test_process_role_messenger():
    message = AsyncMock(spec=types.Message)
    message.text = "Mensajero"
    state = AsyncMock()
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()
    
    await process_role(message, state)
    state.update_data.assert_called_once_with(role="Mensajero")
    message.answer.assert_called_once_with("Por favor, proporciona detalles sobre tu vehículo (marca, modelo, placa):")

@pytest.mark.asyncio
async def test_process_role_client():
    message = AsyncMock(spec=types.Message)
    message.text = "Cliente"
    state = AsyncMock()
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()
    
    await process_role(message, state)
    state.update_data.assert_called_once_with(role="Cliente")
    message.answer.assert_called_once_with("¿Eres una empresa o un particular?", reply_markup=MagicMock())

@pytest.mark.asyncio
async def test_approve_registration():
    message = AsyncMock(spec=types.Message)
    message.reply_to_message = AsyncMock(spec=types.Message)
    message.reply_to_message.photo = [MagicMock()]
    message.reply_to_message.caption = "Usuario: 12345"
    message.bot = AsyncMock()
    message.bot.send_message = AsyncMock()
    message.answer = AsyncMock()
    
    await approve_registration(message)
    message.bot.send_message.assert_called_once_with(12345, "¡Tu registro ha sido aprobado! Bienvenido a Mandadero.")
    message.answer.assert_called_once_with("Registro del usuario 12345 aprobado.")

@pytest.mark.asyncio
async def test_reject_registration():
    message = AsyncMock(spec=types.Message)
    message.reply_to_message = AsyncMock(spec=types.Message)
    message.reply_to_message.photo = [MagicMock()]
    message.reply_to_message.caption = "Usuario: 12345"
    message.bot = AsyncMock()
    message.bot.send_message = AsyncMock()
    message.answer = AsyncMock()
    
    await reject_registration(message)
    message.bot.send_message.assert_called_once_with(12345, "Lo sentimos, tu registro ha sido rechazado. Por favor, contacta al administrador para más información.")
    message.answer.assert_called_once_with("Registro del usuario 12345 rechazado.")