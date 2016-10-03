import discord
import asyncio
import subprocess
client = discord.Client()
def xkcd():
    html = subprocess.Popen('curl xkcd.com', shell=True, stdout=subprocess.PIPE).stdout.read()
    html = html[121:150]
    html = str(html)
    comic_title = ""
    loop = True
    for i in html:
        if loop == True:
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
    return 'https://imgs.xkcd.com/comics/' + comic_title[2:] + '.png'

# A dictionary of basic things for the bot to return. More complex (i.e.
# data-driven) interactions aren't stored here, those go below.
message_index = {
    '!ping': 'Pong!',
    '!hello': 'World!'
}


@client.event
async def on_ready():
    """Run when the bot is ready."""
    print('Logged in as' + client.user.name + ' (ID ' + client.user.id + ').')
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
        else:
            # Respond if the message has a basic, static response.
            # TODO: Apparently 'await' has been replaced in py3 with 'yield from'.
            # Implement this change.
            try:
                await client.send_message(message.channel, message_index[msg])
            except:
                pass


client.run('MjMxNTk1NjEwNjgyMjk0Mjcy.CtCx0g.OhIC5GKMiGM6JMbhos5rQcb8FkE')
