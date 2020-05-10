#  Aura - Discord

Aura is a discord bot focused on rewarding user contributions through
a point system called karma. It has the following features:

* Give out karma on messages containing thanks, ty, thank you case-insensitive
with a single non bot user mention.
* Blacklist and Whitelist Members from giving out karma.
    * Blacklisted Members will get a DM specifying who to contact to dispute it
* Karma Profile with the Profile Picture, full name (name + discriminator) or nick,
total karma and karma breakdown by top x channels configured.
* Cooldown Members from giving out karma after giving it out or set the timer to 0.
* Reset all Karma of a Member in a guild
* Delete karma on message delete of the triggering message.
* Change most configuration on the fly by providing keys from the config.yaml

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

To run this bot you need to manually fill out the following values in the config.yaml

```
token: <Your Bot Account Token>
prefix: <prefix>
role:
    admin: "<Exact Name of Admin role>"
```

Every other value can be updated by executing \<prefix>
config \<key> or config \<key> \<key> etc. for the
according key in the config yaml with a user that has the configured admin role.

## Running the tests

```
pip install pytest-asyncio
pip install mongomock
python -m pytest tests/ or pytest tests/
```

## Dependencies

* see the [requirements file](requirements.txt) for the python app dependencies
* Docker
* Docker-Compose compatible with 3.7
* MongoDB (tested with version 4.2.5)


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