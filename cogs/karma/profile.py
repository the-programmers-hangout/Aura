from discord.ext import commands

from core.service.karma_service import KarmaService
from util.config import ConfigStore


class KarmaProfile(commands.Cog):

    def __init__(self, bot):
        self._bot = bot
        bot.remove_command("help")
        self._karma_service = KarmaService()
        self._configManager = ConfigStore()
        self._config = self._configManager.config