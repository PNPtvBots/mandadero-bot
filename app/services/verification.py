from aiogram import Bot

async def notify_user(user_id, status, bot: Bot):
    if status == 'approved':
        await bot.send_message(user_id, "¡Tu registro ha sido aprobado! Bienvenido a Mandadero.")
    elif status == 'rejected':
        await bot.send_message(user_id, "Lo sentimos, tu registro ha sido rechazado. Por favor, contacta al administrador para más información.")