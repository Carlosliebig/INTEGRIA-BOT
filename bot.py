import os
import pytz
import asyncio
from datetime import datetime
from telegram import Bot
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = os.environ["TELEGRAM_TOKEN"]
MICHAEL_ID = 7227976840

bot = Bot(token=TOKEN)

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
    # Prueba hoy: 12:00, 12:05, 12:10
    objetivos = [
        (12, 0, "🔔 PRUEBA 1 - 12:00: Recordatorio de wellness (solo prueba)"),
        (12, 5, "🔔 PRUEBA 2 - 12:05: Plan nutricional de prueba"),
        (12, 10, "🔔 PRUEBA 3 - 12:10: Recordatorio nocturno de prueba (para validar)")
    ]
    enviados = [False, False, False]

    print("Bot iniciado en modo PRUEBA. Esperando horas: 12:00, 12:05, 12:10...")
    while not all(enviados):
        ahora = datetime.now(chile)
        for i, (h, m, txt) in enumerate(objetivos):
            if not enviados[i] and ahora.hour == h and ahora.minute == m and ahora.second == 0:
                await bot.send_message(chat_id=MICHAEL_ID, text=txt)
                enviados[i] = True
                print(f"Mensaje enviado a las {h:02d}:{m:02d}")
        await asyncio.sleep(30)

    print("Prueba completada. El bot se detendrá ahora (puedes reiniciarlo con nuevo código).")

if __name__ == "__main__":
    import threading
    threading.Thread(target=start_server, daemon=True).start()
    asyncio.run(main())
