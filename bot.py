import os
import pytz
from datetime import datetime
from telegram.ext import Application
from supabase import create_client, Client

# ==================== VARIABLES DE ENTORNO ====================
TOKEN = os.environ["TELEGRAM_TOKEN"]
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
# ==============================================================

# ID de Michael (fijo, también podría ser variable de entorno)
MICHAEL_ID = 7227976840
MICHAEL_EMAIL = "michaelespinoza.arenas@gmail.com"

# Conectar a Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def asegurar_id():
    """Verifica y actualiza el telegram_id de Michael en Supabase."""
    result = supabase.table("arqueros").select("telegram_id").eq("email", MICHAEL_EMAIL).execute()
    if not result.data:
        print(f"⚠️ Email {MICHAEL_EMAIL} no encontrado en la tabla arqueros")
        return
    current = result.data[0]["telegram_id"]
    if current != MICHAEL_ID:
        supabase.table("arqueros").update({"telegram_id": MICHAEL_ID}).eq("email", MICHAEL_EMAIL).execute()
        print(f"✅ Telegram_id actualizado de {current} a {MICHAEL_ID}")
    else:
        print("✅ Telegram_id de Michael ya está correcto")

async def enviar_mensaje(context, texto):
    await context.bot.send_message(chat_id=MICHAEL_ID, text=texto)

async def tarea_1345(context):
    await enviar_mensaje(context, "⏰ Recordatorio 13:45")

async def tarea_1350(context):
    await enviar_mensaje(context, "⏰ Recordatorio 13:50")

async def tarea_1355(context):
    await enviar_mensaje(context, "⏰ Recordatorio 13:55")

def main():
    # Asegurar ID en Supabase
    asegurar_id()
    
    # Crear aplicación
    app = Application.builder().token(TOKEN).build()
    if app.job_queue is None:
        raise RuntimeError("JobQueue no disponible. Asegúrate de instalar 'python-telegram-bot[job-queue]'")
    
    # Zona horaria Chile
    chile = pytz.timezone("America/Santiago")
    hoy = datetime.now(chile).date()
    
    # Definir horas (puedes cambiarlas para probar hoy, por ejemplo a las 14:20, 14:25, 14:30)
    hora_1345 = chile.localize(datetime(hoy.year, hoy.month, hoy.day, 13, 45, 0))
    hora_1350 = chile.localize(datetime(hoy.year, hoy.month, hoy.day, 13, 50, 0))
    hora_1355 = chile.localize(datetime(hoy.year, hoy.month, hoy.day, 13, 55, 0))
    
    # Programar tareas
    app.job_queue.run_once(tarea_1345, when=hora_1345)
    app.job_queue.run_once(tarea_1350, when=hora_1350)
    app.job_queue.run_once(tarea_1355, when=hora_1355)
    
    print(f"Bot iniciado. Mensajes programados para: 13:45, 13:50, 13:55 (hora Chile)")
    print(f"Hoy es {hoy}. Los mensajes se enviarán mañana si ya pasó la hora.")
    app.run_polling()

if __name__ == "__main__":
    main()