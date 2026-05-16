import os
import pytz
from datetime import datetime
from telegram.ext import Application
from supabase import create_client, Client

TOKEN = os.environ["TELEGRAM_TOKEN"]
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

MICHAEL_ID = 7227976840
MICHAEL_EMAIL = "michaelespinoza.arenas@gmail.com"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def asegurar_id():
    result = supabase.table("arqueros").select("telegram_id").eq("email", MICHAEL_EMAIL).execute()
    if not result.data:
        print(f"⚠️ Email {MICHAEL_EMAIL} no encontrado")
        return
    current = result.data[0]["telegram_id"]
    if current != MICHAEL_ID:
        supabase.table("arqueros").update({"telegram_id": MICHAEL_ID}).eq("email", MICHAEL_EMAIL).execute()
        print(f"✅ Actualizado {current} -> {MICHAEL_ID}")
    else:
        print("✅ ID correcto")

async def enviar(context, texto):
    await context.bot.send_message(chat_id=MICHAEL_ID, text=texto)

async def tarea_1(context): await enviar(context, "🔔 Mensaje 1 - 14:50")
async def tarea_2(context): await enviar(context, "🔔 Mensaje 2 - 14:55")
async def tarea_3(context): await enviar(context, "🔔 Mensaje 3 - 15:00")

def main():
    asegurar_id()
    app = Application.builder().token(TOKEN).build()
    if app.job_queue is None:
        raise RuntimeError("JobQueue no disponible. Instala python-telegram-bot[job-queue]")
    chile = pytz.timezone("America/Santiago")
    hoy = datetime.now(chile).date()
    h1 = chile.localize(datetime(hoy.year, hoy.month, hoy.day, 14, 50, 0))
    h2 = chile.localize(datetime(hoy.year, hoy.month, hoy.day, 14, 55, 0))
    h3 = chile.localize(datetime(hoy.year, hoy.month, hoy.day, 15, 0, 0))
    app.job_queue.run_once(tarea_1, when=h1)
    app.job_queue.run_once(tarea_2, when=h2)
    app.job_queue.run_once(tarea_3, when=h3)
    print("Bot iniciado. Mensajes a las 14:50, 14:55, 15:00 (hora Chile)")
    app.run_polling()

if __name__ == "__main__":
    main()
