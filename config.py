try:
    with open('bot_config.txt', 'r') as file:
        for line in file:
            if line.startswith('BOT_TOKEN='):
                BOT_TOKEN = line.replace('BOT_TOKEN=', '').strip()
                break
        else:
            BOT_TOKEN = None
except FileNotFoundError:
    BOT_TOKEN = None