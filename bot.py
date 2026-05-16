import os
import pytz
from datetime import datetime
from telegram.ext import Application

TOKEN = os.environ["TELEGRAM_TOKEN"]
MICHAEL_ID = 7227976840

async def enviar(context, texto):
    await context.bot.send_message(chat_id=MICHAEL_ID, text=texto)

async def tarea_1(context): await enviar(context, "🔔 Prueba 1 - 16:45")
async def tarea_2(context): await enviar(context, "🔔 Prueba 2 - 16:50")
async def tarea_3(context): await enviar(context, "🔔 Prueba 3 - 16:55")

def main():
    app = Application.builder().token(TOKEN).build()
    if app.job_queue is None:
        raise RuntimeError("JobQueue no disponible. Instala python-telegram-bot[job-queue]")
    chile = pytz.timezone("America/Santiago")
    hoy = datetime.now(chile).date()
    h1 = chile.localize(datetime(hoy.year, hoy.month, hoy.day, 16, 45, 0))
    h2 = chile.localize(datetime(hoy.year, hoy.month, hoy.day, 16, 50, 0))
    h3 = chile.localize(datetime(hoy.year, hoy.month, hoy.day, 16, 55, 0))
    app.job_queue.run_once(tarea_1, when=h1)
    app.job_queue.run_once(tarea_2, when=h2)
    app.job_queue.run_once(tarea_3, when=h3)
    print("Bot iniciado. Mensajes a las 16:45, 16:50, 16:55 (hora Chile)")
    app.run_polling()

if __name__ == "__main__":
    main()
