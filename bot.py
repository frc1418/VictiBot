import discord
import asyncio
import configparser
import requests
import json
import re


class VictiBot(discord.Client):
    def __init__(self, config):
        super().__init__()
        self.config = config

        print('Starting VictiBot...')
        self.run(self.config['token'])

    async def on_ready(self):
        """Run when the bot is ready."""
        print('Logged in as ' + self.user.name + ' (ID ' + self.user.id + ').')
        print('------')

        await self.change_presence(status=discord.Status.dnd, game=discord.Game(name='fork me on GitHub @ frc1418/VictiBot!'))

    async def on_message(self, message):
        """Catch a user's messages and figure out what to return."""

        # Log message
        print('- {time} | #{channel} | {user}: {message}'.format(time=message.timestamp.strftime('%y:%m:%d:%H:%M:%S'),
                                                                 channel=message.channel.name,
                                                                 user=message.author.name,
                                                                 message=message.content))

        # Use regex to match the command at the starting of message
        # TODO: Figure out how to match this directly without substringing.
        try:
            cmd = re.search(r'^!(\w+)', message.content).group(0)[1:]
            content = message.content[len(cmd)+2:].split(' ')  # The 2 is for the ! and the space after the command.
        except AttributeError:
            cmd = None
            content = None

        # Only send back message if user that sent the triggering message isn't a bot
        if not message.author.bot:
            if cmd is not None:
                print('INSTRUCTION: %s, %s from %s' % (cmd, content, message.author))
                if cmd == 'about':
                    await self.send_message(message.channel, 'VictiBot is a chatbot for Team 1418\'s Discord server. Bot is currently running as ' + self.user.name + ' (ID ' + self.user.id + '). View on GitHub: https://github.com/frc1418/victibot')
                elif cmd == 'xkcd':
                    # If the user included a specific comic number in their message, get the JSON data for that comic. Otherwise, get the JSON data for the most recent comic.
                    comic = requests.get('http://xkcd.com/' + content[0] + '/info.0.json' if content else 'http://xkcd.com/info.0.json').json()

                    # Send the URL and hover text of the comic.
                    await self.send_message(message.channel, comic['img'])
                    await self.send_message(message.channel, comic['alt'])
                elif cmd == 'nasa':
                    # Get JSON data from NASA APOD API
                    photo = requests.get('https://api.nasa.gov/planetary/apod?api_key=%s' % (self.config['apod_key'] if self.config['apod_key'] else 'DEMO_KEY')).json()

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

            if message.channel.name == 'github':
                print('Message recieved in #github from ' + message.author.name)
                contains_hook = False
                async for msg in self.logs_from(message.channel, limit=6):
                    if msg.author.name == 'GitHub':
                        contains_hook = True
                        break
                if not contains_hook:
                    print('No hook found in past 6 messages, sending warning.')
                    await self.send_message(message.channel, 'Psst... you may want to move to %s.' % self.get_channel('228121923245178880').mention)

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

    victibot = VictiBot(config['bot'])
