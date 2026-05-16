import os
import pytz
import asyncio
from datetime import datetime
from telegram.ext import Application

TOKEN = os.environ["TELEGRAM_TOKEN"]   # Variable de entorno obligatoria
MICHAEL_ID = 7227976840                # ID fijo de Michael

async def enviar(context, texto):
    """Envía un mensaje a Michael"""
    await context.bot.send_message(chat_id=MICHAEL_ID, text=texto)

async def tarea_1(context):
    await enviar(context, "🔔 Recordatorio 15:45")

async def tarea_2(context):
    await enviar(context, "🔔 Recordatorio 15:50")

async def tarea_3(context):
    await enviar(context, "🔔 Recordatorio 15:55")

async def main_async():
    """Función principal asíncrona"""
    app = Application.builder().token(TOKEN).build()
    if app.job_queue is None:
        raise RuntimeError("JobQueue no disponible. Instala python-telegram-bot[job-queue]")

    chile = pytz.timezone("America/Santiago")
    hoy = datetime.now(chile).date()

    # Horarios para hoy
    h1 = chile.localize(datetime(hoy.year, hoy.month, hoy.day, 15, 45, 0))
    h2 = chile.localize(datetime(hoy.year, hoy.month, hoy.day, 15, 50, 0))
    h3 = chile.localize(datetime(hoy.year, hoy.month, hoy.day, 15, 55, 0))

    app.job_queue.run_once(tarea_1, when=h1)
    app.job_queue.run_once(tarea_2, when=h2)
    app.job_queue.run_once(tarea_3, when=h3)

    print("Bot iniciado. Mensajes programados para las 15:45, 15:50 y 15:55 (hora Chile)")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main_async())
