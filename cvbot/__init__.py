import logging
from pathlib import Path

import discord

from . import load
from . import plot
from . import utils
from .cvbot import CoronaVirusBot
from .utils import parse_report

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
            if isinstance(response, str):
                await msg.channel.send(response[:2000])
            elif isinstance(response, Path):
                await msg.channel.send(file=discord.File(response.open('rb')))
