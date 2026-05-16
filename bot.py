import os
import pytz
import asyncio
from datetime import datetime
from telegram.ext import Application
from supabase import create_client, Client

TOKEN = os.environ.get("TELEGRAM_TOKEN")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not all([TOKEN, SUPABASE_URL, SUPABASE_KEY]):
    raise RuntimeError("Faltan variables de entorno")

MICHAEL_ID = 7227976840
MICHAEL_EMAIL = "michaelespinoza.arenas@gmail.com"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def asegurar_id():
    try:
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
    except Exception as e:
        print(f"Error conectando a Supabase: {e}")
        raise

async def enviar(context, texto):
    await context.bot.send_message(chat_id=MICHAEL_ID, text=texto)

async def tarea_1(context): await enviar(context, "🔔 Prueba 1 - 15:15")
async def tarea_2(context): await enviar(context, "🔔 Prueba 2 - 15:20")
async def tarea_3(context): await enviar(context, "🔔 Prueba 3 - 15:25")

def main():
    asegurar_id()
    app = Application.builder().token(TOKEN).build()
    if app.job_queue is None:
        raise RuntimeError("JobQueue no instalado correctamente")
    chile = pytz.timezone("America/Santiago")
    hoy = datetime.now(chile).date()
    h1 = chile.localize(datetime(hoy.year, hoy.month, hoy.day, 15, 15, 0))
    h2 = chile.localize(datetime(hoy.year, hoy.month, hoy.day, 15, 20, 0))
    h3 = chile.localize(datetime(hoy.year, hoy.month, hoy.day, 15, 25, 0))
    app.job_queue.run_once(tarea_1, when=h1)
    app.job_queue.run_once(tarea_2, when=h2)
    app.job_queue.run_once(tarea_3, when=h3)
    print("Bot iniciado. Mensajes a las 15:15, 15:20, 15:25 (hora Chile)")
    app.run_polling()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise
