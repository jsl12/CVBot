import logging
from pathlib import Path

import yaml

from cvbot import cvbot

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    with (Path.cwd() / 'apikey.yaml').open('r') as file:
        token = yaml.load(file, Loader=yaml.SafeLoader)['DISCORD_TOKEN']
    cvbot.run(token)