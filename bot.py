import os
import asyncio
import logging
from datetime import time
import pytz
from telegram import Bot
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────
TOKEN = os.environ.get("TELEGRAM_TOKEN")
TIMEZONE = pytz.timezone("America/Santiago")

# Lista de arqueros: nombre → chat_id
# Agrega aquí a los otros arqueros cuando tengas sus IDs
ARQUEROS = {
    "Michael": os.environ.get("CHAT_ID_MICHAEL", "7227976840"),
    # "Ignacio": os.environ.get("CHAT_ID_IGNACIO", ""),
    # "Lucciano": os.environ.get("CHAT_ID_LUCCIANO", ""),
    # "Bustamante": os.environ.get("CHAT_ID_BUSTAMANTE", ""),
}

# ─── MENSAJES ─────────────────────────────────────────────────────────────────

MENSAJE_8AM = """🟢 *Buenos días, {nombre}!*

Es momento de completar tu *Encuesta Wellness* del día.

📋 Recuerda evaluar:
• 😴 Calidad del sueño
• ⚡ Nivel de energía
• 💪 Fatiga muscular
• 🧠 Estado emocional
• 😣 Dolor o molestias

👉 Completa tu encuesta en INTEGRIA antes de la sesión de hoy.

_Preparador de arqueros Everton de Viña del Mar_"""

MENSAJE_12PM = """🟡 *Recordatorio de mediodía, {nombre}*

⏰ Ya es el momento de tu almuerzo.

🥗 *Recuerda tu plan nutricional:*
• Proteína de calidad (pollo, pescado, pavo)
• Carbohidratos para recargar energía
• Verduras y ensaladas
• Hidratación constante 💧

😴 Si tienes ventana de descanso, *¡aprovéchala!*
Una siesta de 20-30 min mejora tu recuperación.

_INTEGRIA · Everton de Viña del Mar_"""

MENSAJE_8PM = """🌙 *Buenas noches, {nombre}*

Ya es hora de preparar tu recuperación nocturna.

📵 *Protocolo de descanso:*
• Deja el teléfono de lado a las 22:00 hrs
• Evita pantallas al menos 1 hora antes de dormir
• Mantén el cuarto oscuro y fresco
• Intenta dormir entre *8 y 9 horas*

💤 El sueño es tu principal herramienta de recuperación.
Tu rendimiento mañana empieza esta noche.

_INTEGRIA · Everton de Viña del Mar_"""

# ─── FUNCIONES DE ENVÍO ───────────────────────────────────────────────────────

async def enviar_mensaje_a_todos(bot: Bot, mensaje_template: str, contexto: str):
    for nombre, chat_id in ARQUEROS.items():
        if not chat_id:
            logger.warning(f"Sin chat_id para {nombre}, saltando...")
            continue
        try:
            mensaje = mensaje_template.format(nombre=nombre)
            await bot.send_message(
                chat_id=chat_id,
                text=mensaje,
                parse_mode="Markdown"
            )
            logger.info(f"✅ Mensaje {contexto} enviado a {nombre} ({chat_id})")
        except Exception as e:
            logger.error(f"❌ Error enviando a {nombre} ({chat_id}): {e}")

async def job_8am(context: ContextTypes.DEFAULT_TYPE):
    await enviar_mensaje_a_todos(context.bot, MENSAJE_8AM, "8AM")

async def job_12pm(context: ContextTypes.DEFAULT_TYPE):
    await enviar_mensaje_a_todos(context.bot, MENSAJE_12PM, "12PM")

async def job_8pm(context: ContextTypes.DEFAULT_TYPE):
    await enviar_mensaje_a_todos(context.bot, MENSAJE_8PM, "8PM")

# ─── COMANDOS ─────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    nombre = update.effective_user.first_name
    await update.message.reply_text(
        f"✅ *INTEGRIA Bot activo*\n\n"
        f"Hola {nombre}! Tu Chat ID es: `{chat_id}`\n\n"
        f"Recibirás mensajes a las 8:00, 12:00 y 20:00 hrs (hora Chile).",
        parse_mode="Markdown"
    )
    logger.info(f"Nuevo usuario: {nombre} | Chat ID: {chat_id}")

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando de prueba para verificar que el bot funciona"""
    await update.message.reply_text(
        "🟢 *INTEGRIA Bot funcionando correctamente*\n\n"
        "Los mensajes programados están activos:\n"
        "• 8:00 AM — Encuesta Wellness\n"
        "• 12:00 PM — Plan nutricional\n"
        "• 8:00 PM — Protocolo de descanso",
        parse_mode="Markdown"
    )

async def enviar_ahora(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envía todos los mensajes ahora mismo (para testear)"""
    await update.message.reply_text("📤 Enviando mensajes de prueba a todos los arqueros...")
    await enviar_mensaje_a_todos(context.bot, MENSAJE_8AM, "TEST-8AM")
    await enviar_mensaje_a_todos(context.bot, MENSAJE_12PM, "TEST-12PM")
    await enviar_mensaje_a_todos(context.bot, MENSAJE_8PM, "TEST-8PM")
    await update.message.reply_text("✅ Mensajes de prueba enviados.")

# ─── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    if not TOKEN:
        raise ValueError("❌ TELEGRAM_TOKEN no está configurado en las variables de entorno")

    app = Application.builder().token(TOKEN).build()

    # Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(CommandHandler("enviar_ahora", enviar_ahora))

    # Horarios programados (hora Chile = America/Santiago)
    job_queue = app.job_queue
    job_queue.run_daily(job_8am,  time=time(hour=8,  minute=0, tzinfo=TIMEZONE), name="wellness_8am")
    job_queue.run_daily(job_12pm, time=time(hour=12, minute=0, tzinfo=TIMEZONE), name="nutricion_12pm")
    job_queue.run_daily(job_8pm,  time=time(hour=20, minute=0, tzinfo=TIMEZONE), name="descanso_8pm")

    logger.info("🚀 INTEGRIA Bot iniciado — mensajes programados 8AM, 12PM, 8PM (Santiago)")
    app.run_polling(allowed_updates=["message"])

if __name__ == "__main__":
    main()
