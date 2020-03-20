import logging
import re
from pathlib import Path

import discord
import pandas as pd
import yaml

from .load import death_stats, confirmed_stats

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
            if '#usadeaths' in msg.content:
                return f'{death_stats()["US"].max().sum()}'
            elif '#txdeaths' in msg.content:
                return f'{death_stats()["US"]["Texas"].max().sum()}'

    @property
    def deaths(self) -> pd.DataFrame:
        return death_stats()

    @property
    def confirmed(self) -> pd.DataFrame:
        return confirmed_stats()
