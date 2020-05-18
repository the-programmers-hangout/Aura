import logging

from discord.ext import commands
from discord.ext.commands import when_mentioned_or

from cogs.error import CommandErrorHandler
from cogs.help import HelpMenu
from cogs.karma.profile import KarmaProfile
from cogs.karma.producer import KarmaProducer
from cogs.karma.reduce import KarmaReducer, KarmaBlocker
from cogs.settings import SettingsManager
from util.config import config, read_config

if __name__ == '__main__':
    read_config()
    client = commands.Bot(command_prefix=when_mentioned_or(config['prefix']))
    client.remove_command('help')
    client.add_cog(KarmaProducer(client))
    client.add_cog(KarmaBlocker(client))
    client.add_cog(KarmaReducer(client))
    client.add_cog(KarmaProfile(client))
    client.add_cog(SettingsManager(client))
    client.add_cog(CommandErrorHandler(client))
    client.add_cog(HelpMenu(client))
    logging.basicConfig(level=config['logging'], format='%(levelname)s %(name)s %(message)s')
    client.run(config['token'])
