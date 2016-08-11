import discord
import ftplib
import logging
import os
from urllib import request


TOKEN = open('token', 'r').readline().replace('\n', '')

FORMATS = ['jpg', 'bmp', 'png', 'gif', 'tiff']

class picSaver(discord.Client):
    forbidden_channels = []
    def __init__(self):
        super().__init__()

    def run(self):
        super().run(TOKEN, bot=True)

    def writeText(self, message):
        if os.stat('messages').st_size > 10**4:
            self.sendPicture('messages')
            os.remove('messages')
        with open('messages', 'a') as fp:
            author = message.author.display_name
            discrim = message.author.discriminator
            fp.write(''.join([str(message.timestamp), ':',author, '#', discrim, message.clean_content]))
            logging.info('message saved')


    def sendPicture(self, pic_name):
        try:
            t = ftplib.FTP('192.168.1.231')
            t.cwd('/yobabot')
            t.storbinary('STOR ' + pic_name, open(pic_name, 'rb'))
            logging.info('Picture saved' + pic_name)
        except:
            logging.error('Could not send pic ' + pic_name)

    def checkAndSafe(self, message):
        if message.channel in self.forbidden_channels:
            return
        pic_saver_mentions = [t for t in message.mentions if t.name == 'pictureSaver']
        if pic_saver_mentions != [] and 'stop' in message.clean_content:
            self.forbidden_channels.append(message.channel)
            return
        if message.embeds is not None:
            for emb in message.embeds:
                format = ''
                for f in FORMATS:
                    if '.' + f in emb['url']:
                        format = f
                        break
                filename = ''.join([str(message.timestamp), '.', format])
                with open(filename, 'wb') as f:
                    try:
                        req = request.Request(emb['url'], headers={'User-Agent': 'Mozilla/5.0'})
                    except:
                        logging.error('Could not get picture')
                    else:
                        f.write(request.urlopen(req).read())
                        self.sendPicture(filename)
                        try:
                            os.remove(filename)
                        except:
                            logging.error('Could not remove file' + filename)

    def on_message(self, message):
        self.writeText(message)
        self.checkAndSafe(message)

    def on_message_edit(self, before, after):
        self.writeText(after)
        self.checkAndSafe(after)

if __name__ == '__main__':
    logging.basicConfig(filename='discordBot.log', format='%(asctime)s - %(levelname)s - %(message)s',level=logging.INFO)
    bot = picSaver()
    bot.run()
