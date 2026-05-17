import os
import pytz
import asyncio
from datetime import datetime
from telegram import Bot

TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN no configurado")

MICHAEL_ID = 7227976840
bot = Bot(token=TOKEN)

async def enviar_mensaje(texto):
    try:
        await bot.send_message(chat_id=MICHAEL_ID, text=texto)
        print(f"Mensaje enviado: {texto}")
    except Exception as e:
        print(f"Error al enviar: {e}")

async def main():
    chile = pytz.timezone("America/Santiago")
    ultimo_envio = {
        "wellness": None,
        "nutricion": None,
        "noche": None,
        "prueba1": None,
        "prueba2": None,
        "prueba3": None
    }
    print("Bot iniciado. Esperando horarios...")
    while True:
        try:
            ahora = datetime.now(chile)
            hoy = ahora.date()
            hora_min = (ahora.hour, ahora.minute)

            # Pruebas hoy 17 de mayo (12:30, 12:35, 12:40) - ya pasaron, pero las dejamos por si acaso
            if hoy == datetime(2026, 5, 17).date():
                if hora_min == (12, 30) and ultimo_envio["prueba1"] != hoy:
                    await enviar_mensaje("🔔 PRUEBA 1 - 12:30")
                    ultimo_envio["prueba1"] = hoy
                if hora_min == (12, 35) and ultimo_envio["prueba2"] != hoy:
                    await enviar_mensaje("🔔 PRUEBA 2 - 12:35")
                    ultimo_envio["prueba2"] = hoy
                if hora_min == (12, 40) and ultimo_envio["prueba3"] != hoy:
                    await enviar_mensaje("🔔 PRUEBA 3 - 12:40")
                    ultimo_envio["prueba3"] = hoy

            # Horarios regulares (todos los días)
            if hora_min == (8, 0) and ultimo_envio["wellness"] != hoy:
                await enviar_mensaje("🌞 ¡Buenos días! No olvides responder la encuesta de wellness.")
                ultimo_envio["wellness"] = hoy
            if hora_min == (12, 0) and ultimo_envio["nutricion"] != hoy:
                await enviar_mensaje("🍽️ Plan nutricional de Michael: 200g proteína, 2 tazas verduras, sin carbohidratos en la cena.")
                ultimo_envio["nutricion"] = hoy
            if hora_min == (20, 0) and ultimo_envio["noche"] != hoy:
                await enviar_mensaje("🌙 Es hora de descansar. Apaga pantallas, relájate y duerme bien.")
                ultimo_envio["noche"] = hoy

            await asyncio.sleep(30)
        except Exception as e:
            print(f"Error en bucle principal: {e}")
            await asyncio.sleep(10)

if __name__ == "__main__":
    # Bucle infinito que reinicia el main si por alguna razón termina
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            print(f"Error fatal, reiniciando en 10s: {e}")
            import time
            time.sleep(10)
