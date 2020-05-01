import yaml
from discord.ext import commands

from cogs.karma.profile import KarmaProfile
from cogs.karma.provider import KarmaProvider
from cogs.karma.reset import KarmaManager
from cogs.settings import SettingsManager

if __name__ == '__main__':
    with open("config.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    client = commands.Bot(command_prefix=data_loaded['prefix'])
    client.add_cog(KarmaProvider(client))
    client.add_cog(KarmaManager(client))
    client.add_cog(KarmaProfile(client))
    client.add_cog(SettingsManager(client))
    client.run(data_loaded['token'])
