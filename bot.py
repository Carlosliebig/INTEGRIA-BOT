import os
import logging
from datetime import time
import pytz
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TIMEZONE = pytz.timezone("America/Santiago")

ARQUEROS = {
    "Michael": os.environ.get("CHAT_ID_MICHAEL", "7227976840"),
}

MENSAJE_8AM = """Buenos dias {nombre}!

Es momento de completar tu Encuesta Wellness del dia.

Recuerda evaluar:
- Calidad del sueno
- Nivel de energia
- Fatiga muscular
- Estado emocional
- Dolor o molestias

Completa tu encuesta en INTEGRIA antes de la sesion de hoy.

Preparador de arqueros Everton de Vina del Mar"""

MENSAJE_12PM = """Recordatorio de mediodia, {nombre}

Ya es el momento de tu almuerzo.

Recuerda tu plan nutricional:
- Proteina de calidad (pollo, pescado, pavo)
- Carbohidratos para recargar energia
- Verduras y ensaladas
- Hidratacion constante

Si tienes ventana de descanso aprovechala!
Una siesta de 20-30 min mejora tu recuperacion.

INTEGRIA - Everton de Vina del Mar"""

MENSAJE_8PM = """Buenas noches, {nombre}

Ya es hora de preparar tu recuperacion nocturna.

Protocolo de descanso:
- Deja el telefono de lado a las 22:00 hrs
- Evita pantallas al menos 1 hora antes de dormir
- Manten el cuarto oscuro y fresco
- Intenta dormir entre 8 y 9 horas

El sueno es tu principal herramienta de recuperacion.
Tu rendimiento manana empieza esta noche.

INTEGRIA - Everton de Vina del Mar"""


async def enviar_a_todos(bot: Bot, template: str, tag: str):
    for nombre, chat_id in ARQUEROS.items():
        if not chat_id:
            continue
        try:
            await bot.send_message(
                chat_id=int(chat_id),
                text=template.format(nombre=nombre)
            )
            logger.info(f"OK {tag} -> {nombre}")
        except Exception as e:
            logger.error(f"ERROR {tag} -> {nombre}: {e}")


async def job_8am(context: ContextTypes.DEFAULT_TYPE):
    await enviar_a_todos(context.bot, MENSAJE_8AM, "8AM")

async def job_12pm(context: ContextTypes.DEFAULT_TYPE):
    await enviar_a_todos(context.bot, MENSAJE_12PM, "12PM")

async def job_8pm(context: ContextTypes.DEFAULT_TYPE):
    await enviar_a_todos(context.bot, MENSAJE_8PM, "8PM")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    nombre = update.effective_user.first_name
    await update.message.reply_text(
        f"INTEGRIA Bot activo\n\nHola {nombre}! Tu Chat ID es: {chat_id}\n\nRecibiras mensajes a las 8:00, 12:00 y 20:00 hrs (hora Chile)."
    )
    logger.info(f"Start: {nombre} | {chat_id}")


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "INTEGRIA Bot funcionando correctamente.\n\nMensajes programados:\n- 8:00 AM Encuesta Wellness\n- 12:00 PM Plan nutricional\n- 8:00 PM Protocolo de descanso"
    )


async def enviar_ahora(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Enviando mensajes de prueba...")
    await enviar_a_todos(context.bot, MENSAJE_8AM, "TEST-8AM")
    await enviar_a_todos(context.bot, MENSAJE_12PM, "TEST-12PM")
    await enviar_a_todos(context.bot, MENSAJE_8PM, "TEST-8PM")
    await update.message.reply_text("Mensajes enviados correctamente.")


def main():
    if not TOKEN:
        logger.error("TELEGRAM_TOKEN no encontrado")
        raise SystemExit(1)

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(CommandHandler("enviar_ahora", enviar_ahora))

    jq = app.job_queue
    jq.run_daily(job_8am,  time=time(8,  0, tzinfo=TIMEZONE))
    jq.run_daily(job_12pm, time=time(12, 0, tzinfo=TIMEZONE))
    jq.run_daily(job_8pm,  time=time(20, 0, tzinfo=TIMEZONE))

    logger.info("INTEGRIA Bot iniciado")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
