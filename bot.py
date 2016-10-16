# Import various libraries
import discord
import asyncio
import subprocess
import requests
import json

# Initialize bot client
# TODO: Make bot a class like normal bots.
client = discord.Client()

#bot prefix
PREFIX = '!'

# A dictionary of basic things for the bot to return. More complex (i.e.
# data-driven) interactions aren't stored here, those go below.
messageIndex = {
    Prefix + 'ping': 'Pong!',
    Prefix + 'hello': 'World!',
    'rickroll': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'xcq': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    Prefix + 'balloumoji': ':bigdissapointment::moustache::ballouminatti::1982::nope::notapproved::fedora1::happy::flowers::notbad::soundboard:',
    'it\'s time to stop': 'https://www.youtube.com/watch?v=2k0SmqbBIpQ',
    'stop': 'https://www.youtube.com/watch?v=2k0SmqbBIpQ'
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
        if msg.startswith(PREFIX + 'about'):
            await client.send_message(message.channel, 'Victibot is a chatbot for Team 1418\'s Discord server. Bot is currently running as ' + client.user.name + ' (ID ' + client.user.id + '). View on GitHub: https://github.com/ErikBoesen/victibot')
        elif msg.startswith(PREFIX + 'xkcd'):
            # Store the number/other content after the '!xkcd '.
            comic = msg[6:]

            # If the user included a specific comic number in their message, get the JSON data for that comic. Otherwise, get the JSON data for the most recent comic.
            r = requests.get('http://xkcd.com/' + comic + '/info.0.json' if comic else 'http://xkcd.com/info.0.json')

            # Send the URL of the image from the JSON fetched above.
            await client.send_message(message.channel, r.json()['img'])
        elif msg == (PREFIX + 'update'):
            # Confirm that the bot is updating
            await client.send_message(message.channel, 'Updating...')
            # Start a git pull to update bot
            print(str(subprocess.Popen('git pull', shell=True, stdout=subprocess.PIPE).stdout.read()))
        else:
            # Respond if the message has a basic, static response.
            # TODO: Apparently 'await' has been replaced in py3 with 'yield from'.
            # Implement this change.
            try:
                await client.send_message(message.channel, messageIndex[msg])
            except:
                pass


@client.event
async def on_member_join(member):
    await client.send_message(member.server.default_channel, '**Welcome ' + member.mention + ' to the ' + member.server.name + ' server!**')


@client.event
async def on_member_remove(member):
    await client.send_message(member.server.default_channel, member.name + ' left the server :frowning: RIP ' + member.name)


# Get token from token.txt.
with open('token.txt', 'r') as token_file:
    # Parse into a string, and get rid of trailing newlines.
    token = token_file.read().replace('\n', '')

print('Starting with token ' + token + '...')

# Start bot!
client.run(token)

# That's all, folks.
