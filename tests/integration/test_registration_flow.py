import pytest
from unittest.mock import AsyncMock, MagicMock
from aiogram import types
from aiogram.dispatcher import Dispatcher
from app.handlers.start import start, register_handlers as register_start_handlers
from app.handlers.registration import register_handlers as register_registration_handlers
from app.handlers.admin import register_handlers as register_admin_handlers

@pytest.mark.asyncio
async def test_registration_flow():
    dp = Dispatcher()
    register_start_handlers(dp)
    register_registration_handlers(dp)
    register_admin_handlers(dp)
    
    # Simulate /start command
    message = AsyncMock(spec=types.Message)
    message.text = "/start"
    message.answer = AsyncMock()
    
    # Call start handler
    await start(message)
    message.answer.assert_called_once()

@pytest.mark.asyncio
async def test_admin_approval_flow():
    dp = Dispatcher()
    register_admin_handlers(dp)
    
    # Simulate admin approving a registration
    message = AsyncMock(spec=types.Message)
    message.reply_to_message = AsyncMock(spec=types.Message)
    message.reply_to_message.photo = [MagicMock()]
    message.reply_to_message.caption = "Usuario: 12345"
    message.bot = AsyncMock()
    message.bot.send_message = AsyncMock()
    message.answer = AsyncMock()
    
    await approve_registration(message)
    message.bot.send_message.assert_called_once_with(12345, "¡Tu registro ha sido aprobado! Bienvenido a Mandadero.")