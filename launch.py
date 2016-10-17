execute = True
while execute == True:
    with open("bot.py") as f:
        code = compile(f.read(), "bot.py", 'exec')
        exec(code)
