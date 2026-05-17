import os, logging, sys
from datetime import time
import pytz
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TIMEZONE = pytz.timezone("America/Santiago")
ARQUEROS = {"Michael": os.environ.get("CHAT_ID_MICHAEL", "7227976840")}

MSG_8AM = "Buenos dias {nombre}!\n\nCompleta tu Encuesta Wellness en INTEGRIA antes de la sesion de hoy.\n\nEvalua sueno, energia, fatiga y estado emocional.\n\nINTEGRIA - Everton Vina del Mar"
MSG_12PM = "Hola {nombre}!\n\nRecuerda tu almuerzo:\n- Proteina de calidad\n- Carbohidratos\n- Verduras\n- Hidratacion\n\nDescansa 20-30 min si puedes.\n\nINTEGRIA - Everton"
MSG_8PM = "Buenas noches {nombre}!\n\nProtocolo de descanso:\n- Sin pantallas desde las 22:00\n- Cuarto oscuro y fresco\n- Dormir 8-9 horas\n\nINTEGRIA - Everton"

async def enviar(bot, template, tag):
    for nombre, chat_id in ARQUEROS.items():
        if not chat_id: continue
        try:
            await bot.send_message(chat_id=int(chat_id), text=template.format(nombre=nombre))
            logger.info(f"OK {tag} {nombre}")
        except Exception as e:
            logger.error(f"ERROR {tag} {nombre}: {e}")

async def job_8am(ctx): await enviar(ctx.bot, MSG_8AM, "8AM")
async def job_12pm(ctx): await enviar(ctx.bot, MSG_12PM, "12PM")
async def job_8pm(ctx): await enviar(ctx.bot, MSG_8PM, "8PM")

async def start(update: Update, ctx):
    cid = update.effective_chat.id
    nombre = update.effective_user.first_name
    await update.message.reply_text(f"INTEGRIA Bot activo! Hola {nombre}, tu Chat ID es: {cid}")

async def test(update: Update, ctx):
    await update.message.reply_text("INTEGRIA Bot funcionando OK.")

async def enviar_ahora(update: Update, ctx):
    await update.message.reply_text("Enviando prueba...")
    await enviar(ctx.bot, MSG_8AM, "T8AM")
    await enviar(ctx.bot, MSG_12PM, "T12PM")
    await enviar(ctx.bot, MSG_8PM, "T8PM")
    await update.message.reply_text("Listo!")

def main():
    logger.info(f"Iniciando - TOKEN presente: {bool(TOKEN)}")
    if not TOKEN:
        logger.error("ERROR: sin TELEGRAM_TOKEN")
        sys.exit(1)
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(CommandHandler("enviar_ahora", enviar_ahora))
    app.job_queue.run_daily(job_8am,  time=time(8,  0, tzinfo=TIMEZONE))
    app.job_queue.run_daily(job_12pm, time=time(12, 0, tzinfo=TIMEZONE))
    app.job_queue.run_daily(job_8pm,  time=time(20, 0, tzinfo=TIMEZONE))
    logger.info("Bot corriendo!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
