import discord
import asyncio
import subprocess
import os
client = discord.Client()
fd = os.open("token.txt",os.O_RDWR)
token = os.read(fd,100)[2:62]
token = (str(token)[2:61])
def xkcd():
    htmlo = subprocess.Popen('curl xkcd.com', shell=True, stdout=subprocess.PIPE).stdout.read()
    html = htmlo[121:150]
    html = str(html)
    comic_title = ""
    loop = True
    for i in html:
        if loop:
            if not i == '<':
                print (i)
                comic_title += str(i)
            else:
                loop = False
            if i == "'":
                print('whyyyyy!!!!')
    print (comic_title)
    print ('curl -O imgs.xkcd.com/comics/' + comic_title + '.png')
    comic_title = comic_title.lower()
    titletext = ''
    loop = True
    print (titletext)
    for a in str(htmlo[2805:]):
        if loop:
            if not a == '"':
                print (a)
                titletext += str(a)
            else:
                print ('something else happened')
                loop = False
    print (titletext)
    return titletext[2:] + '\nhttps://imgs.xkcd.com/comics/' + comic_title[2:] + '.png'

# A dictionary of basic things for the bot to return. More complex (i.e.
# data-driven) interactions aren't stored here, those go below.
message_index = {
    '!ping': 'Pong!',
    '!hello': 'World!',
    'rickroll': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'xcq': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
}


@client.event
async def on_ready():
    """Run when the bot is ready."""
    print('Logged in as ' + client.user.name + ' (ID ' + client.user.id + ').')
    print('------')


@client.event
async def on_message(message):
    """Catch a user's messages and figure out what to return."""

    msg = message.content.lower()

    # Only send back message if user that sent the triggering message isn't a bot
    if not message.author.bot:
        # Special returns!
        if msg.startswith('!about'):
            await client.send_message(message.channel, 'Victibot is a chatbot for Team 1418\'s Discord server. Bot is currently running as ' + client.user.name + ' (ID ' + client.user.id + '). View on GitHub: https://github.com/ErikBoesen/victibot')
        elif msg.startswith('hey victibot'):
            await client.send_message(message.channel, 'Thanks, but I\'m not Siri (yet).')
        elif msg.startswith('ok victibot') or msg.startswith('okay victibot'):
            await client.send_message(message.channel, 'Thanks, but I\'m not Google Now (yet).')
        elif msg.startswith('xcq') or msg.startswith('rickroll'):
            await client.send_message(message.channel, 'Never Gonna Give You Up - Rick Astley: \n https://www.youtube.com/watch?v=dQw4w9WgXcQ')
        elif msg.startswith('xkcd'):
            await client.send_message(message.channel,  (xkcd()))
        elif msg == 'it\'s time to stop' or msg == 'minecraft' or msg == 'league of legends' or msg == 'stop':
            await client.send_message(message.channel, 'https://www.youtube.com/watch?v=2k0SmqbBIpQ')
        elif msg == '!update':
            await client.send_message(message.channel, 'Updating...')
            print str(subprocess.Popen('git checkout HEAD bot.py', shell=True, stdout=subprocess.PIPE).stdout.read())
        else:
            # Respond if the message has a basic, static response.
            # TODO: Apparently 'await' has been replaced in py3 with 'yield from'.
            # Implement this change.
            try:
                await client.send_message(message.channel, message_index[msg])
            except:
                pass


client.run(token)
