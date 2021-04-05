import discord
from discord.ext import commands
from discord.ext.commands import when_mentioned_or

from cogs.general.help import Help, KarmaTutor
from cogs.general.module import ModuleManager
from cogs.general.permission import PermissionManager
from cogs.general.settings import SettingsManager
from cogs.karma.leaderboard import KarmaLeaderboard
from cogs.karma.producer import KarmaProducer
from cogs.karma.profile import KarmaProfile
from cogs.karma.reduce import KarmaReducer, KarmaBlocker
from util.config import config
from util.constants import cog_map


class Aura(commands.AutoShardedBot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True

        super().__init__(command_prefix=when_mentioned_or(config["prefix"]),
                         description="Aura collecting karma...", pm_help=None,
                         help_attrs=dict(hidden=True), fetch_offline_members=True,
                         heartbeat_timeout=150.0, intents=intents)

        self.remove_command('help')
        module_manager = ModuleManager(self)
        karma_producer = KarmaProducer(self)
        karma_blocker = KarmaBlocker(self)
        karma_reducer = KarmaReducer(self)
        karma_profile = KarmaProfile(self)
        karma_leaderboard = KarmaLeaderboard(self)
        settings_manager = SettingsManager(self)
        help_cog = Help(self)
        karma_tutor = KarmaTutor(self)

        self.add_cog(module_manager)
        self.add_cog(karma_producer)
        self.add_cog(karma_blocker)
        self.add_cog(karma_reducer)
        self.add_cog(karma_profile)
        self.add_cog(karma_leaderboard)
        self.add_cog(settings_manager)
        self.add_cog(help_cog)
        self.add_cog(karma_tutor)
        self.add_cog(PermissionManager(self))

        cog_map["ModuleManager"] = module_manager
        cog_map["KarmaProducer"] = karma_producer
        cog_map["KarmaBlocker"] = karma_blocker
        cog_map["KarmaReducer"] = karma_reducer
        cog_map["KarmaProfile"] = karma_profile
        cog_map["KarmaLeaderboard"] = karma_leaderboard
        cog_map["SettingsManager"] = settings_manager
        cog_map["Help"] = help_cog
        cog_map["KarmaTutor"] = karma_tutor

    def run(self):
        super().run(config["token"], reconnect=True)



