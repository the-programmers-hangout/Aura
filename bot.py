import logging
import sys

from discord.ext import commands
from discord.ext.commands import when_mentioned_or

from cogs.general.error import CommandErrorHandler
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

logging.basicConfig(level=config['logging'],
                    format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    stream=sys.stdout)

if __name__ == '__main__':
    client = commands.Bot(command_prefix=when_mentioned_or(config['prefix']))
    client.remove_command('help')
    module_manager = ModuleManager(client)
    karma_producer = KarmaProducer(client)
    karma_blocker = KarmaBlocker(client)
    karma_reducer = KarmaReducer(client)
    karma_profile = KarmaProfile(client)
    karma_leaderboard = KarmaLeaderboard(client)
    settings_manager = SettingsManager(client)
    help_cog = Help(client)
    karma_tutor = KarmaTutor(client)

    client.add_cog(module_manager)
    client.add_cog(karma_producer)
    client.add_cog(karma_blocker)
    client.add_cog(karma_reducer)
    client.add_cog(karma_profile)
    client.add_cog(karma_leaderboard)
    client.add_cog(settings_manager)
    client.add_cog(CommandErrorHandler(client))
    client.add_cog(help_cog)
    client.add_cog(karma_tutor)
    client.add_cog(PermissionManager(client))

    cog_map['ModuleManager'] = module_manager
    cog_map['KarmaProducer'] = karma_producer
    cog_map['KarmaBlocker'] = karma_blocker
    cog_map['KarmaReducer'] = karma_reducer
    cog_map['KarmaProfile'] = karma_profile
    cog_map['KarmaLeaderboard'] = karma_leaderboard
    cog_map['SettingsManager'] = settings_manager
    cog_map['Help'] = help_cog
    cog_map['KarmaTutor'] = karma_tutor

    client.run(config['token'])
