import discord
import asyncio

client = discord.Client()


# A dictionary of basic things for the bot to return. More complex (i.e.
# data-driven) interactions aren't stored here, those go below.
message_index = {
    '!ping': 'Pong!',
    '!hello': 'World!'
}


@client.event
async def on_ready():
    """Run when the bot is ready."""
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    """Catch a user's messages and figure out what to return."""
    # TODO: Prevent bot from triggering itself.

    # Special returns!
    if message.content.lower().startswith('!about'):
        await client.send_message(message.channel, 'Victibot is a chatbot for Team 1418\'s Discord server. Bot is currently running as ' + client.user.name + ' (ID ' + client.user.id + '). View on GitHub: https://github.com/ErikBoesen/victibot')
    elif message.content.lower().startswith('hey victibot'):
        await client.send_message(message.channel, 'Thanks, but I\'m not Siri (yet).')
    elif message.content.lower().startswith('ok victibot') or message.content.lower().startswith('okay victibot'):
        await client.send_message(message.channel, 'Thanks, but I\'m not Google Now (yet).')
    elif message.content.lower().startswith('xcq') or message.content.lower().startswith('rickroll'):
        await client.send_message(message.channel, 'Never Gonna Give You Up - Rick Astley: \n https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    elif message.content.lower().startswith('h') or message.content.lower().startswith('H'):
        await client.send_message(message.channel, 'H has been pressed. H4X1N6 1MM1N3N7.')
    else:
        # Respond if the message has a basic, static response.
        # TODO: Apparently 'await' has been replaced in py3 with 'yield from'.
        # Implement this change.
        try:
            await client.send_message(message.channel, message_index[message.content.lower()])
        except:
            pass

client.run('MjMxNTk1NjEwNjgyMjk0Mjcy.CtCx0g.OhIC5GKMiGM6JMbhos5rQcb8FkE')
