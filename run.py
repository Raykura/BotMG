from flask import Flask
from threading import Thread
from highrise.__main__ import *
import time
from asyncio import run as arun

class WebServer:
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route('/')
        def index() -> str:
            return "Funcionando"

    def run(self) -> None:
        self.app.run(host='0.0.0.0', port=8084)

    def keep_alive(self):
        t = Thread(target=self.run)
        t.start()

class RunBot:
    room_id = "66d2726b2e80dd1f614c4dbb"  # Your room ID
    bot_token = "202d7b11c3d00fe44e472d4c1b8ad9f4e3277e5fd03927d5cfab15532e9d8af8"  # Your bot token
    bot_file = "main"
    bot_class = "Bot"

    def __init__(self) -> None:
        self.definitions = [
            BotDefinition(
                getattr(import_module(self.bot_file), self.bot_class)(),
                self.room_id, self.bot_token)
        ]

    def run_bot(self) -> None:
        try:
            # Start the bot
            arun(main(self.definitions))
        except Exception as e:
            print(f"Error: {e}")
            # Prevent immediate rejoin by introducing a longer delay
            time.sleep(30)  # Wait 30 seconds before attempting to reconnect
            print("Attempting to reconnect...")
            self.run_bot()  # Recursively try to run the bot again after failure

if __name__ == "__main__":
    WebServer().keep_alive()
    RunBot().run_bot()
