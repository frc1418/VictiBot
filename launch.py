execute = True
while execute == True:
    if (subprocess.Popen('cat run', shell=True, stdout=subprocess.PIPE).stdout.read()) == "1":
        subprocess.Popen('killall bot', shell=True, stdout=subprocess.PIPE).stdout.read()
        subprocess.Popen('python3 bot.py&', shell=True, stdout=subprocess.PIPE).stdout.read()
