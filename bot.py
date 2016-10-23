# Import various libraries
import discord
import asyncio
import subprocess
import requests
import json
import os
# Initialize bot client
# TODO: Make bot a class like normal bots.
client = discord.Client()

# bot prefix
PREFIX = '!'

# Two dictionaries (prefix commands and text triggers) of basic things for the bot to return. More complex (i.e.
# data-driven) interactions aren't stored here, those go below.
prefixMessageIndex = {
    # Returns the corresponding value if preceeded by the PREFIX
    PREFIX + 'ping': 'Pong!',
    PREFIX + 'hello': 'World!',
    PREFIX + 'balloumoji': '<:bigdissapointment:236086062617853953><:moustache:236092022312665089><:ballouminatti:236132317603561475><:1982:236092769779712000><:nope:236096818180653057><:notapproved:236096861113417728><:fedora1:236131582468030474><:happy:236137265305223168><:flowers:236139383764418560><:notbad:236140764416049152><:soundboard:236147928547328000>',

}
messageIndex = {
    # Returns the corresponding text unless it interferes with a command beginning with the PREFIX
    'rickroll': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'xcq': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'it\'s time to stop': 'https://www.youtube.com/watch?v=2k0SmqbBIpQ',
    'stop': 'https://www.youtube.com/watch?v=2k0SmqbBIpQ'
}

helpMessage = """Welcome to VictiBot!
              The commands are
              !ping
              !hello
              !balloumoji
              !about
              !help
              rickroll
              xcq
              it\'s time to stop
              stop

              Type one of these into the chat to try it out"""


@client.async_event
def on_ready():
    """Run when the bot is ready."""
    print('Logged in as ' + client.user.name + ' (ID ' + client.user.id + ').')
    print('------')
    # Turns out this is annoying
    # yield from client.send_message(client.get_channel('228121885630529536'), 'Victibot is online and ready! Currently running as ' + client.user.name + ' (ID ' + client.user.id + ').')


@client.async_event
def on_message(message):
    """Catch a user's messages and figure out what to return."""
    msg = message.content.lower()

    # Only send back message if user that sent the triggering message isn't a bot
    if not message.author.bot:
        # Special returns!
        if msg.startswith(PREFIX + 'about'):
            yield from client.send_message(message.channel, 'Victibot is a chatbot for Team 1418\'s Discord server. Bot is currently running as ' + client.user.name + ' (ID ' + client.user.id + '). View on GitHub: https://github.com/ErikBoesen/victibot')
        elif msg.startswith('xkcd'):
            # Store the number/other content after the '!xkcd '.
            comic = msg[5:]

            # If the user included a specific comic number in their message, get the JSON data for that comic. Otherwise, get the JSON data for the most recent comic.
            r = requests.get('http://xkcd.com/' + comic + '/info.0.json' if comic else 'http://xkcd.com/info.0.json')

            # Send the URL of the image from the JSON fetched above.
            # The title text is half of the comic
            yield from client.send_message(message.channel, r.json()['img'])
            yield from client.send_message(message.channel, r.json()['alt'])
        elif msg.startswith(PREFIX + 'nasa'):
            # Grab JSON data from apod
            r = requests.get('https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY')

            # Send URL for image along with image's title
            yield from client.send_message(message.channel, r.json()['url'])
            yield from client.send_message(message.channel, r.json()['title'])
        elif msg == (PREFIX + 'update'):
            # Confirm that the bot is updating
            yield from client.send_message(message.channel, 'Updating...')
            # Start a git pull to update bot
            print(str(subprocess.Popen('git pull', shell=True, stdout=subprocess.PIPE).stdout.read()))
            yield from client.send_message(message.channel, 'Update Successful! Restarting...')
            # Restart
            subprocess.Popen('python3 bot.py', shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
            os.abort()
        elif message.content.isupper() and len(message.content) > 5:
            # if someone sends a message in all caps, respond with a friendly reminder
            yield from client.send_message(message.channel, "did that _really_ need to be in all caps?")
        elif msg.startswith('!help'):
            yield from client.send_message(message.author, helpMessage)
        else:
            # Respond if the message has a basic, static response.
            # TODO: Apparently 'yield from' has been replaced in py3 with 'yield from'.
            # Implement this change.
            try:
                # Prefix commands take priority over standard text commands
                yield from client.send_message(message.channel, prefixMessageIndex[(msg)])
                print ('Prefix Done')
            except:
                try:
                    yield from client.send_message(message.channel, messageIndex[msg])
                except:
                    pass


@client.async_event
def on_member_join(member):
    yield from client.send_message(member.server.default_channel, '**Welcome ' + member.mention + ' to the ' + member.server.name + ' server!**')


@client.async_event
def on_member_remove(member):
    yield from client.send_message(member.server.default_channel, member.name + ' left the server :frowning: RIP ' + member.name)


# Get token from token.txt.
with open('token.txt', 'r') as token_file:
    # Parse into a string, and get rid of trailing newlines.
    token = token_file.read().replace('\n', '')

print('Starting with token ' + token + '...')

# Start bot!
client.run(token)

# That's all, folks.
