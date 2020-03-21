import logging

import discord

from . import load
from . import utils
from .cvbot import CoronaVirusBot
from cvbot.utils import parse_report

logger = logging.getLogger(__name__)

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
            await msg.channel.send(response[:2000])
