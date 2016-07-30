import discord
from urllib import request


TOKEN = open('token', 'r').readline()

FORMATS = ['jpg', 'bmp', 'png', 'gif', 'tiff']

class picSaver(discord.Client):
    def __init__(self):
        super().__init__()

    def run(self):
        super().run(TOKEN, bot=True)

    def checkAndSafe(self, message):
        if message.embeds is not None:
            for emb in message.embeds:
                format = ''
                for f in FORMATS:
                    if '.' + f in emb['url']:
                        format = f
                        break
                filename = ''.join([str(message.timestamp), '.', format])
                with open(filename, 'wb') as f:
                    req = request.Request(emb['url'], headers={'User-Agent': 'Mozilla/5.0'})
                    f.write(request.urlopen(req).read())

    async def on_message(self, message):
        self.checkAndSafe(message)

    def on_message_edit(self, before, after):
        self.checkAndSafe(after)

if __name__ == '__main__':
    bot = picSaver()
    bot.run()