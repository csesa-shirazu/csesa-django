import telepot
from telepot.loop import MessageLoop
from csesa_telegram.settings import PROXY, TELEGRAM_BOT_TOKEN
from time import sleep


def handle(msg):
    pass


bot = telepot.Bot(TELEGRAM_BOT_TOKEN)
MessageLoop(bot, handle).run_as_thread()

