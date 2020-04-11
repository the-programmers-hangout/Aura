from discord.ext import commands

from util.config import ConfigManager


class SetupManager(commands.Cog):

    def __init__(self, bot):
        self._bot = bot
        self._configManager = ConfigManager()
        self._config = self._configManager.config

