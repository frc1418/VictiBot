import discord
import asyncio

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    print(message.author)
    #if not message.author == 'VictiBot#7518')d:
    def interaction(input):
        # This function will be
        # Stuff do do when people ask questions to the bot (i.e. 'where is the robot code' or 'are there any upcoming deadlines', etc...)
        # I don't mean like siri, but it would be cool to have a bot that is actually helpful

        message_index = {
            'Hello': 'World',
            'VictiBot': 'Victibot is a work-in-progress chatbot for the team 1418 server. More info on GitHub at https://github.com/ErikBoesen/victibot'
        }
        try:
            return message_index[input]
        except:
            pass

    # This stuff is for special commands that require the bot to do more than just respond with an answer
    # We should standardize this so that all commands begin with a ! or something like that
    if message.content.startswith('!test'):
        # TODO: Apparently await has been replaced with yield from.
        await client.send_message(message.channel, 'Received test, Victibot is running')
    elif message.content.startswith('about'):
        await client.send_message(message.channel, 'Running as ' + client.user.name +  '(' + client.user.id + '). Victibot is a work-in-progress chatbot for the team 1418 server. More info on GitHub at https://github.com/ErikBoesen/victibot')
    else:
        output = interaction(message.content);
        if not output == None:
            await client.send_message(message.channel, output)

client.run('MjMxNTk1NjEwNjgyMjk0Mjcy.CtCx0g.OhIC5GKMiGM6JMbhos5rQcb8FkE')
