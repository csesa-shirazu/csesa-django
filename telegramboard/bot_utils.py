import telepot
from telepot.loop import MessageLoop
from csesa.settings import PROXY, TELEGRAM_BOT_TOKEN
from time import sleep


def handle(msg):
    pass

if PROXY:
    telepot.api.set_proxy(PROXY)

bot = telepot.Bot(TELEGRAM_BOT_TOKEN)
# MessageLoop(bot, handle).run_as_thread()

