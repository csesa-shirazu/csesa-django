import telepot
from telepot.loop import MessageLoop
from csesa.settings import PROXY, TELEGRAM_BOT_TOKEN

def handle(msg):
    pass


if PROXY:
    telepot.api.set_proxy(PROXY)

bot = telepot.Bot(TELEGRAM_BOT_TOKEN)
bot_loop = MessageLoop(bot, handle)