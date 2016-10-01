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
    #This tells the bot not to do anything if a special command is called
    skip_interaction = False

    def interaction(input):
        #Stuff do do when people ask questions to the bot (i.e. 'where is the robot code' or 'are there any upcoming deadlines', etc...)
        #I don't mean like siri, but it would be cool to have a bot that is actually helpful
        if input = "Hello"
            return "World"

    #This stuff is for special commands that require the bot to do more than just respond with an answer
    #We should standardize this so that all commands begin with a ! or something like that
    if message.content.startswith('!test'):
        client.send_message(message.channel, 'Received test, Victibot is running')
        skip_interaction = True
    if message.content.startswith('about'):
        client.send_message(message.channel, 'Running as ' + client.user.name +  '(' + client.user.id + '). Victibot is a work-in-progress chatbot for the team 1418 server. More info on github at https://github.com/ErikBoesen/victibot')
        skip_interaction = True
    if message.content.startswith('!debug_mode')
        skip_interaction = True
        #Set some variable to do something for some purpose

    #Respond to user questions with answers from the interction function
    if skip_interaction = False:
        client.send_message(message.channel, interaction(message.content))

client.run('')
