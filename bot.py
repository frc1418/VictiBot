import discord
import asyncio
import configparser
import requests
import json
import re


class VictiBot(discord.Client):
    def __init__(self):
        super().__init__()

        print('Starting VictiBot...')

    async def on_ready(self):
        """Run when the bot is ready."""
        print('Logged in as ' + self.user.name + ' (ID ' + self.user.id + ').')
        print('------')

        await self.change_presence(status=discord.Status.dnd, game=discord.Game(name='fork me on GitHub @ frc1418/VictiBot!'))

    async def on_message(self, message):
        """Catch a user's messages and figure out what to return."""
        # Use regex to match the command at the starting of a
        # TODO: Figure out how to match this directly without substringing.
        try:
            cmd = re.search(r'^!(\w+)', message.content).group(0)[1:]
            content = message.content[len(cmd)+2:]  # The 2 is for the ! and the space after the command.
        except AttributeError:
            cmd = None
            content = None

        # Only send back message if user that sent the triggering message isn't a bot
        if not message.author.bot and cmd is not None:
            print('Recieved command %s' % cmd)
            if cmd == 'about':
                await self.send_message(message.channel, 'VictiBot is a chatbot for Team 1418\'s Discord server. Bot is currently running as ' + self.user.name + ' (ID ' + self.user.id + '). View on GitHub: https://github.com/frc1418/victibot')
            elif cmd == 'xkcd':
                # If the user included a specific comic number in their message, get the JSON data for that comic. Otherwise, get the JSON data for the most recent comic.
                comic = requests.get('http://xkcd.com/' + content + '/info.0.json' if content else 'http://xkcd.com/info.0.json').json()

                # Send the URL and hover text of the comic.
                await self.send_message(message.channel, comic['img'])
                await self.send_message(message.channel, comic['alt'])
            elif cmd == 'nasa':
                # Get JSON data from apod
                photo = requests.get('https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY').json()

                # Send URL for image along with image's title
                await self.send_message(message.channel, photo['url'])
                await self.send_message(message.channel, photo['title'])
            elif cmd == 'help':
                # PM the user a help message.
                await self.send_message(message.author, open('help.md').read())
            else:
                # Respond if the message has a basic, static response.
                try:
                    with open('commands.json') as f:
                        commands = json.load(f)
                    await self.send_message(message.channel, commands[cmd])
                except KeyError:
                    pass

    async def on_member_join(self, member):
        """
        When a member joins a server.

        :param member: The name of the member who joined.
        """
        await self.send_message(member.server.default_channel, '**Welcome ' + member.mention + ' to the server!** :rocket:')

    async def on_member_remove(self, member):
        """
        When a member has left or been kicked from a server.

        :param member: The name of the member who left.
        """
        await self.send_message(member.server.default_channel, member.name + ' has left the server. :frowning:')


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    victibot = VictiBot()
    victibot.run(config['bot']['token'])
