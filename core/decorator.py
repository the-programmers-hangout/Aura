import logging

from discord.ext.commands import check

from util.config import config, roles
from util.permission import permission_map
from util.util import member_has_role

log = logging.getLogger(__name__)


def has_required_role(command_name):
    """
    decorator to check if member has the required role
    :param command_name: of the command
    :return: if the required role is on the user calling this command
    """

    def predicate(ctx):
        role = str(permission_map[command_name])
        caller = ctx.message.author
        log.info(f'Checking on permission {role} for command: {command_name} and user: {ctx.message.author.id}')
        if role.lower() == 'everyone':
            return True
        elif role.lower() == 'owner':
            if caller.id == int(config['owner']):
                return True
        elif role.lower() == 'moderator':
            if member_has_role(caller, roles()['moderator']) \
                    or member_has_role(caller, roles()['admin']) \
                    or caller.id == int(config['owner']):
                return True
        elif role.lower() == 'admin':
            if member_has_role(caller, roles()['admin']) \
                    or caller.id == int(config['owner']):
                return True
        return False
    return check(predicate)
