import os
import pytz
import asyncio
from datetime import datetime
from telegram import Bot

TOKEN = os.environ["TELEGRAM_TOKEN"]
MICHAEL_ID = 7227976840

bot = Bot(token=TOKEN)

async def enviar_mensaje(texto):
    await bot.send_message(chat_id=MICHAEL_ID, text=texto)

async def main():
    chile = pytz.timezone("America/Santiago")
    # Horas objetivo: 17:00, 17:05, 17:10 (ajústalas si quieres)
    objetivos = [(17, 0, "🔔 Prueba 1 - 17:00"),
                 (17, 5, "🔔 Prueba 2 - 17:05"),
                 (17, 10, "🔔 Prueba 3 - 17:10")]
    enviados = [False, False, False]

    print("Bot iniciado. Esperando horas...")
    while not all(enviados):
        ahora = datetime.now(chile)
        for i, (h, m, txt) in enumerate(objetivos):
            if not enviados[i] and ahora.hour == h and ahora.minute == m and ahora.second == 0:
                await enviar_mensaje(txt)
                enviados[i] = True
                print(f"Mensaje enviado a las {h:02d}:{m:02d}")
        await asyncio.sleep(30)  # Revisa cada 30 segundos

if __name__ == "__main__":
    asyncio.run(main())
