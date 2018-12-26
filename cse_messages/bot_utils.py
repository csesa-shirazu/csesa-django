import telepot
from telepot.loop import MessageLoop
from cse_messages.settings import PROXY, TOKEN

def handle(msg):
    pass


if PROXY:
    telepot.api.set_proxy(PROXY)

bot = telepot.Bot(TOKEN)
bot_loop = MessageLoop(bot, handle)