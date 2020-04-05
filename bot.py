import yaml
from discord.ext import commands

from cogs.karma import Karma

if __name__ == '__main__':
    with open("config.yaml", 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    client = commands.Bot(command_prefix=data_loaded['prefix'])
    client.add_cog(Karma(client, 'helpful'))
    client.add_cog(Karma(client, 'informative'))
    client.add_cog(Karma(client, 'funny'))
    client.add_cog(Karma(client, 'kind'))
    client.add_cog(Karma(client, 'creative'))
    client.run(data_loaded['token'])
