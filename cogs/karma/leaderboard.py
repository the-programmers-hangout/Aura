import discord
from discord.ext import commands

from core.service.karma_service import KarmaService
from util.config import ConfigStore


class Leaderboard(commands.Cog):

    def __init__(self, bot):
        self._bot = bot
        bot.remove_command("help")
        self._karma_service = KarmaService()
        self._configManager = ConfigStore()
        self._config = self._configManager.config
        self._limit = self._config['leaderboard']['limit']

    @commands.command(name='leaderboard')
    async def get_top_karma_members(self, ctx, karma_type):
        if karma_type in self._configManager.karma_categories:
            guild_id: str = self._config['guild']
            print(guild_id)
            embed = discord.Embed(title="{}".format(karma_type).capitalize(),
                                  description="Top {} Members with {} karma".format(self._limit, karma_type),
                                  color=0x00ff00)
            leaderboard = self._karma_service.get_top_karma_members(guild_id, karma_type)
            if leaderboard.collection.count_documents(dict(guild_id=guild_id)) > 0:
                for document in leaderboard:
                    guild = self._bot.get_guild(int(guild_id))
                    member = guild.get_member(int(document['member_id']))
                    karma = document['karma']
                    embed.add_field(name=member.name+'#'+member.discriminator, value=karma, inline=False)
                await ctx.channel.send(embed=embed)
            else:
                await ctx.channel.send('At present there is not a single user with {} karma'.format(karma_type))
        else:
            await ctx.channel.send('Karma Type not recognized, only following are valid karma types {}'
                                   .format(self._configManager.karma_categories))

