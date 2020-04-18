import yaml
from discord.ext import commands

from cogs.karma.checker import KarmaChecker
from cogs.karma.reset import KarmaCleaner
from cogs.settings import SettingsManager

if __name__ == '__main__':
    with open("config.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    client = commands.Bot(command_prefix=data_loaded['prefix'])
    client.add_cog(KarmaChecker(client))
    client.add_cog(KarmaCleaner(client))
    client.add_cog(SettingsManager(client))
    client.run(data_loaded['token'])
