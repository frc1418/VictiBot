execute = True
while execute == True:
    try:
        with open("bot.py") as f:
            code = compile(f.read(), "bot.py", 'exec')
            exec(code)
        except:
            print ("an error ocurred")
