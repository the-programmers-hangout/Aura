import logging
import sys

from discord.ext import commands
from discord.ext.commands import when_mentioned_or

from cogs.error import CommandErrorHandler
from cogs.help import HelpMenu
from cogs.karma.producer import KarmaProducer
from cogs.karma.profile import KarmaProfile
from cogs.karma.reduce import KarmaReducer, KarmaBlocker
from cogs.settings import SettingsManager
from util.config import config

logging.basicConfig(level=config['logging'], format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    stream=sys.stdout)

if __name__ == '__main__':
    client = commands.Bot(command_prefix=when_mentioned_or(config['prefix']))
    client.remove_command('help')
    client.add_cog(KarmaProducer(client))
    client.add_cog(KarmaBlocker(client))
    client.add_cog(KarmaReducer(client))
    client.add_cog(KarmaProfile(client))
    client.add_cog(SettingsManager(client))
    client.add_cog(CommandErrorHandler(client))
    client.add_cog(HelpMenu(client))
    client.run(config['token'])