#  Aura - Discord Karma Bot

Aura is a discord bot focused on rewarding user contributions through
an arbitrary point system called karma. It has the following features:

* Give out karma on messages containing a custom list of case-insensitive keywords.
    * Cooldowns are applied one-way to each pair of thankee-giver, that means that the giver-thankee can
    swap while the cooldown of thankee-giver is still ticking.
    * Ignores invalid mentions like: self author mentions, bot mentions, bot thanking other users.
    * Ignores messages containing discord greentext, keywords enclosed in quatation marks.
* Configurable Feedback on karma gain
    * Logging to a channel.
    * Thumbs up reaction to the message.
    * Affirmation Message in same channel as the thank you message.
    * or all of the above.
* Blacklist and Whitelist Members from giving out karma.
    * Blacklisted Members on trying to give karma will get a DM specifying who to contact to dispute it.
* Get Karma of one or multiple Members through Mentions, or user id's.
    * self karma requires no arguments.
* Karma Profile with the Discord Profile Picture, full name (name + discriminator) or nick,
total karma and karma breakdown by top x channels configured.
    * single mention only.
    * self profile requires no arguments.
* Karma Leaderboard globally or per channel
 * provide optional argument of days to get a time restricted leaderboard
* Reset all Karma of a Member in a guild, this currently has no undo functionality.
* Delete karma from Members on message delete, reaction clear and reaction removal.
* Change most configuration on the fly by providing keys from the config.yaml.
* Module Model, enable and disable features you don't need or like.
* Karma Help Commands to provide you with all the information on aura and how it works,
what configuration parameters mean etc.
* Change Permission of every command but the help command, disable the help module if you don't need it.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

This Bot requires a privileged intent: members.
This Bot requires a mongodb database

To run this bot you need to manually fill out the following values in the config.yaml.example
or create config.yaml with the following fields filled out.
If you are filling out the example file, you can use the create_config python file to create a config.yaml
out of the example file.
```
token: <Your Bot Account Token>
prefix: <prefix>
role:
    admin: "<Exact Name of Admin role>"
owner: <id of bot-owner>
everything under the database key
```

Every other value can be updated by executing \<prefix>
config \<key> or config \<key> \<key> etc. for the
according key in the config yaml with a user that has the configured admin role.

## Running it locally
Since this bot has a docker-compose file, all you need to start your own Aura locally is:
```
docker-compose up --build
```
or
```
docker-compose down ; docker-compose build ; docker-compose up
```
while being in the root directory of aura.

## Running the tests

```
pip install mongomock
python -m pytest tests/ or pytest tests/
```

## Requirements

* see the [requirements file](pyproject.toml) for the python app dependencies
* Docker
* Docker-Compose compatible with 3.7
* MongoDB (at least 4.2.5)


## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to the project.

## Versioning

This project uses [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/arkencl/aura/tags/). 

## Authors

* **Georg Göring** - *Original Author* - [arkencl](https://github.com/arkencl)

See also the list of [contributors](https://github.com/arkencl/aura/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

### Attribution

This README.MD is adapted from the following [Template][template].

[template]: https://gist.github.com/PurpleBooth/109311bb0361f32d87a2
