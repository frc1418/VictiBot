import os

# Kill bot and open a new process.
# TODO: Find a better way of doing this.
os.system('killall bot')
os.system('python3 bot.py')
