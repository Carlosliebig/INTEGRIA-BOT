import os
import pytz
import asyncio
from datetime import datetime
from telegram import Bot
from http.server import HTTPServer, BaseHTTPRequestHandler

# Token correcto (obtenido de BotFather)
TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN no configurado")

MICHAEL_ID = 7227976840
bot = Bot(token=TOKEN)

# Servidor HTTP para mantener Railway activo
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot activo")

def start_server():
    port = int(os.environ.get("PORT", 8000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

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
        ahora = datetime.now(chile)
        hoy = ahora.date()
        hora_min = (ahora.hour, ahora.minute)

        # PRUEBAS HOY (12:30, 12:35, 12:40) - solo 17 de mayo
        if hoy == datetime(2026, 5, 17).date():
            if hora_min == (12, 30) and ultimo_envio["prueba1"] != hoy:
                await bot.send_message(chat_id=MICHAEL_ID, text="🔔 PRUEBA 1 - 12:30")
                ultimo_envio["prueba1"] = hoy
                print("Prueba 1 enviada")
            if hora_min == (12, 35) and ultimo_envio["prueba2"] != hoy:
                await bot.send_message(chat_id=MICHAEL_ID, text="🔔 PRUEBA 2 - 12:35")
                ultimo_envio["prueba2"] = hoy
                print("Prueba 2 enviada")
            if hora_min == (12, 40) and ultimo_envio["prueba3"] != hoy:
                await bot.send_message(chat_id=MICHAEL_ID, text="🔔 PRUEBA 3 - 12:40")
                ultimo_envio["prueba3"] = hoy
                print("Prueba 3 enviada")

        # HORARIOS REGULARES (todos los días)
        if hora_min == (8, 0) and ultimo_envio["wellness"] != hoy:
            await bot.send_message(chat_id=MICHAEL_ID, text="🌞 ¡Buenos días! No olvides responder la encuesta de wellness.")
            ultimo_envio["wellness"] = hoy
            print("Wellness enviado")
        if hora_min == (12, 0) and ultimo_envio["nutricion"] != hoy:
            await bot.send_message(chat_id=MICHAEL_ID, text="🍽️ Plan nutricional de Michael: 200g proteína, 2 tazas verduras, sin carbohidratos en la cena.")
            ultimo_envio["nutricion"] = hoy
            print("Plan nutricional enviado")
        if hora_min == (20, 0) and ultimo_envio["noche"] != hoy:
            await bot.send_message(chat_id=MICHAEL_ID, text="🌙 Es hora de descansar. Apaga pantallas, relájate y duerme bien.")
            ultimo_envio["noche"] = hoy
            print("Recordatorio nocturno enviado")

        await asyncio.sleep(30)

if __name__ == "__main__":
    import threading
    threading.Thread(target=start_server, daemon=True).start()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot detenido manualmente")
