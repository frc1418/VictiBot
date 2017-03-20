import discord
import asyncio
import requests
import json
import os
import re


class VictiBot(discord.Client):
    def __init__(self):
        """
        Initialize bot.

        :param token: Bot account token.
        """
        super().__init__()

        print('Starting VictiBot...')

    async def on_ready(self):
        """Run when the bot is ready."""
        print('Logged in as ' + self.user.name + ' (ID ' + self.user.id + ').')
        print('------')

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
                r = requests.get('http://xkcd.com/' + content + '/info.0.json' if content else 'http://xkcd.com/info.0.json')

                # Send the URL of the image from the JSON fetched above.
                # The title text is half of the comic
                await self.send_message(message.channel, r.json()['img'])
                await self.send_message(message.channel, r.json()['alt'])
            elif cmd == 'nasa':
                # Grab JSON data from apod
                r = requests.get('https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY')

                # Send URL for image along with image's title
                await self.send_message(message.channel, r.json()['url'])
                await self.send_message(message.channel, r.json()['title'])
            elif cmd == 'update':
                # Confirm that the bot is updating
                await self.send_message(message.channel, 'Updating...')
                # Start a git pull to update bot
                print(str(subprocess.Popen('git pull', shell=True, stdout=subprocess.PIPE).stdout.read()))
                await self.send_message(message.channel, 'Update Successful! Restarting...')
                # Restart
                subprocess.Popen('python3 bot.py', shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
                os.abort()
            elif cmd == 'help':
                # PM the user a help message.
                await self.send_message(message.author, open('help.md').read())
            else:
                # Respond if the message has a basic, static response.
                try:
                    # Prefix commands take priority over standard text commands
                    await self.send_message(message.channel, {
                        'ping': 'Pong!',
                        'hello': 'World!',
                        'balloumoji': '<:bigdissapointment:236086062617853953><:moustache:236092022312665089><:ballouminatti:236132317603561475><:1982:236092769779712000><:nope:236096818180653057><:notapproved:236096861113417728><:fedora1:236131582468030474><:happy:236137265305223168><:flowers:236139383764418560><:timmyffs:237378458366377986><:notbad:236140764416049152><:soundboard:236147928547328000>',
                    }[cmd])
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
    token = open('token.txt', 'r').read().replace('\n', '')

    victibot = VictiBot()
    victibot.run(token)
