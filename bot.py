import os
import pytz
import asyncio
from datetime import datetime
from telegram import Bot
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = os.environ["TELEGRAM_TOKEN"]
MICHAEL_ID = 7227976840

bot = Bot(token=TOKEN)

# Servidor HTTP dummy para que Render mantenga el servicio activo
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), DummyHandler)
    server.serve_forever()

async def enviar_mensaje(texto):
    await bot.send_message(chat_id=MICHAEL_ID, text=texto)

async def main():
    chile = pytz.timezone("America/Santiago")
    # Horas para hoy: 16:00, 16:05, 16:10
    objetivos = [(16, 0, "🔔 Prueba 1 - 16:00"),
                 (16, 5, "🔔 Prueba 2 - 16:05"),
                 (16, 10, "🔔 Prueba 3 - 16:10")]
    enviados = [False, False, False]

    print("Bot iniciado. Esperando horas...")
    while not all(enviados):
        ahora = datetime.now(chile)
        for i, (h, m, txt) in enumerate(objetivos):
            if not enviados[i] and ahora.hour == h and ahora.minute == m and ahora.second == 0:
                await enviar_mensaje(txt)
                enviados[i] = True
                print(f"Mensaje enviado a las {h:02d}:{m:02d}")
        await asyncio.sleep(30)

if __name__ == "__main__":
    import threading
    threading.Thread(target=run_http_server, daemon=True).start()
    asyncio.run(main())
