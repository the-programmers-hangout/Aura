#  Aura

Aura is a discord bot focused on rewarding user contributions through simple karma.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

To run this bot you need to manually fill out the following values in the config.yaml

```
token: <Your Bot Account Token>
prefix: <prefix>
role:
    admin: "<Exact Name of Admin role>"
```

Every other value can be filled or updated by executing \<prefix> 
config \<key> or config \<key> \<key> etc. for the
according key in the config yaml with a user that has the configured admin role.

## Running the tests

TBD

## Dependencies

* see the [requirements file](requirements.txt)
* Docker
* Docker-Compose

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to the project.

## Versioning

This project uses [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/arkencl/aura/tags/). 

## Authors

* **Georg Göring** - *Initial work* - [arkencl](https://github.com/arkencl)

See also the list of [contributors](https://github.com/arkencl/aura/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

### Attribution

This README.MD is adapted from the following [Template][template].

[template]: https://gist.github.com/PurpleBooth/109311bb0361f32d87a2