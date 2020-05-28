from collections import defaultdict
from copy import deepcopy

import yaml


def read_config():
    with open("config.yaml", 'r') as stream:
        return yaml.safe_load(stream)


config = read_config()


def write_config():
    with open("config.yaml", 'w') as stream:
        yaml.safe_dump(config, stream)


# shorthand for roles configuration
def roles():
    return config['roles']


# shorthand for profile configurations
def profile():
    return config['profile']


# shorthand for blacklist configuration
def blacklist():
    return config['blacklist']


# shorthand for karma configuration
def karma():
    return config['karma']


# split the karma keywords
def thanks_list():
    return config['karma']['keywords'].split(",")


# version dict
def version():
    return dict(aura_version='1.4.4', python_version='3.8.2', discord_version='1.3.3')


# return the discord tag of the author of this bot
def author_discord():
    return 'arkencl#5579'


# return the link to the repository
def repository():
    return '[[Github]](https://github.com/arkencl/aura)'


class ConfigDescription:
    def __init__(self, description, values=None):
        if values is None:
            self.values = ['true', 'false']
        else:
            self.values: [] = values  # possible values
        self.description: str = description  # 'which channel aura should log karma gain, removals and other messages'


descriptions = deepcopy(config)
descriptions['blacklist']['emote'] = ConfigDescription('should aura react with a skull on blacklisted giver messages')
descriptions['blacklist']['dm'] = ConfigDescription('should aura dm the blacklisted member that he is blacklisted'
                                                    + ', if this is set you have to change blacklist contact')
descriptions['blacklist']['contact'] = ConfigDescription('who to mention in the blacklist dm to contact for the user'
                                                         + ' to resolve his blacklist', ['Any String'])
descriptions['karma']['emote'] = ConfigDescription('should aura react with a thumps up emoji on karma gain')
descriptions['karma']['log'] = ConfigDescription('should aura log karma gain messages')
descriptions['karma']['message'] = ConfigDescription('should aura respond with a mention message'
                                                     + ' right where the karma gain happened')
descriptions['karma']['time-emote'] = ConfigDescription('should aura react with a clock if the giver-receiver '
                                                        + ' combination is'
                                                        + ' on cooldown')
descriptions['karma']['time-message'] = ConfigDescription('should aura send a cooldown message in the channel of'
                                                          + ' the attempted karma message')
descriptions['karma']['keywords'] = ConfigDescription('the karma keyword list to check messages for',
                                                      ['thanks,ty,thank you'])

descriptions['profile']['channels'] = ConfigDescription('how many top channels to include in profile',
                                                        ['Any positive number including 0'])

descriptions['roles']['admin'] = ConfigDescription('admin role can change configuration and do all of the'
                                                   + 'commands', ['Admin'])

descriptions['roles']['moderator'] = ConfigDescription('staff role can do anything but configure the bot',
                                                       ['Staff'])

descriptions['cooldown'] = ConfigDescription('Cooldown applied to karma thanks message in seconds',
                                             ['Any positive number including 0'])

descriptions['channel']['log'] = ConfigDescription('which channel to post log messages to',
                                                   ['Any channel id'])

descriptions['karma']['edit'] = ConfigDescription('whether aura should track message edits for karma gain / deletion'
                                                  + '\n' + 'currently only supports' +
                                                           ' messages that were karma messages before but aren\'t'
                                                           + ' after the edit or'
                                                           + ' become karma messages after the edit but weren\'t before'
                                                  )
