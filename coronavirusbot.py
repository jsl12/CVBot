import logging
from pathlib import Path
import re
import discord
import yaml

logger = logging.getLogger(__name__)

class CoronaVirusBot:
    REGEX = re.compile(f'(corona|virus)', re.IGNORECASE)

    def __init__(self):
        self.client = discord.Client()
        return

    def run(self, apikey: str):
        self.client.run(apikey)

    def process_message(self, msg: discord.Message):
        m = self.REGEX.search(msg.content)
        if m is not None:
            return f"found 'corona' or 'virus' in a message from {msg.author}"

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    yaml_path = Path(r'D:\Discord\coronavirusbot\apikey.yaml')
    CHANNEL_WHITELIST = ['robotics-facility']

    with yaml_path.open('r') as file:
        apikey = yaml.load(file, Loader=yaml.SafeLoader)['DISCORD_TOKEN']

    cvbot = CoronaVirusBot()

    @cvbot.client.event
    async def on_ready():
        logger.info(f'ready as {cvbot.client.user}')

    @cvbot.client.event
    async def on_message(msg: discord.Message):
        if msg.author == cvbot.client.user:
            return
        elif msg.channel.name != 'robotics-facility':
            return
        else:
            response = cvbot.process_message(msg)
            if response is not None:
                await msg.channel.send(response)

    cvbot.run(apikey)
