import logging

from discord.ext import commands

log = logging.getLogger(__name__)


# based on gist https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612
class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error) -> None:
        """
        Command Error Handler listening to the command error event.
        :param ctx: context of the invocation
        :param error: error which was thrown
        :return: None
        """
        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound, commands.UserInputError)

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            return await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')

        log.error('Ignoring exception in command {}: {}'.format(ctx.command, error))
