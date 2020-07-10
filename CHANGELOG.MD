## Version History

Version History for Aura

### 0.1.0

-   Give [karma category type] command implemented
-   Configuration.yaml created and filled
-   User feedback for correct usage of the [give karma] command
-   User feedback for incorrect usage of the [give karma] command
-   Filtering role mentions
-   Filtering messages with more than one mention
-   Filtering messages without a user mention, this includes everyone and here mentions.
-   Bot can be started through Docker.

### 0.2.0

-   Docker-compose setup with database complete with database
    dashboard, mongodb and discord bot.
-   Leaderboard : get single of type implemented
-   Leaderboard : get top x of type implemented
-   Karma Service: upsert implemented
-   Karma Service: get implemented
-   Karma Service: filter top x of karma type implemented
-   Karma cooldown user after executing give [karma category type] successfully
-   Filtering other bot mentions

### 0.3.0

-   retrieve database configuration from config.yaml
-   centralize configuration into its own class
-   get karma [karma_type] returns karma for message author

### 0.4.0

-   add command to reset karma of member (all in guild)
-   add command to reset karma of member (type in guild)
-   add role configuration to the bot

### 0.5.0

-   modify get karma command to be executed with the respective category command without introducing a separate command
-   first version of a README.md
-   added contributor.MD

### 0.6.0 rework version

-   remove karma category commands
-   detect karma by thanks @user and variations
-   remove leaderboard functionality
-   remove karma type from service and model classes
-   add channel_id to model classes and services
-   add commands to change the configuration on the fly
-   aggregate karma on karma without any arguments
-   remove karma on message delete
-   log karma in specific channel

### 0.7.0 profiles

-   update documentation
-   convert config into module level variable / methods
-   blacklist / whitelist members
-   add karma profile embed (member.name+#+member.discriminator, top x karma channels + karma for each)
-   move guild out of config and get it from the message
-   add help command back in and add default descriptions
-   add profile picture to profile embed
-   various profile embed improvements (proper spacing etc.)

### 0.8.0 blacklist dm

-   dm users that are blacklisted when they try to give out karma
-   improve config command:
    -   check for non existent configuration parameters
    -   filter out certain configuration parameters (prefix and token)

### 0.9.0 small reworks, config embed, configuration changes, reactions, tests, logging, error

-   add some exception handling
-   add logging to aura
-   add config embed
-   make sure aura works only inside of guilds by adding guild checks
-   make it possible to thank several people in a message
-   make it possible to get the karma of several mentions in a message
-   add check on nickname for profile
-   add nickname to profile
-   add emote thumps up to thanks messages
-   add config in regards to show how karma was received
-   add tests for every major functionality that does not require mocking the discord library
-   refactor core model classes

### 0.9.1

-   fix karma give not working

### 1.0.0 release version

-   tidy up code

### 1.1.0 config and help command

-   rework help command
-   change some config command values
-   add prefix and mention of bot for commands

### 1.1.1

-   hotfix reset command

### 1.1.2

-   hotfix double karma bug

### 1.1.3

-   hotfix karma mention

### 1.1.4

-   hotfix message author karma thanks

### 1.1.5

-   fix logging
-   fix profile and karma messages with bot mention and id usage
-   fix blacklist, whitelist, reset with bot mention and id usage

### 1.1.6

-   fix reset method AGAIN

### 1.1.7

-   let conversion return a set of members to prevent spamming

### 1.1.8

-   fix multiple karma thanks filter out duplicates

### 1.1.9

-   add message link to log messages of karma gain

### 1.1.10

-   fix profile not working with args

### 1.1.11

-   fix profile taking not only the first user arg

### 1.2.0 embed and reaction removal event

-   add information embed on @mention of bot
-   remove karma on removing the reaction

### 1.2.1

-   fix karma on message deletion not working correctly

### 1.3.0 cooldown, thank you keywords configureable

-   thank you keyword list configureable
-   cooldown based on giver-receiver instead of only giver
-   log karma deletes into the log as well

### 1.3.1

-   fix message delete await validate message
-   fix version string in info embed

### 1.4.0

-   rework config menu
-   make deletion logging more consistent
-   add config help command

### 1.4.1

-   fix some help config descriptions

### 1.4.2

-   fix version string in info embed

### 1.4.3

-   fix config help embed formatting

### 1.4.4

-   fix version string in info embed

### 1.5.0

-   filter out messages where the thanks is inside of " "
-   track partial message edits
-   add ways for normal members to revoke karma given out
-   fix profile embed spacing
-   fix config embed spacing
-   add command to view all blacklisted members

### 1.5.1

-   again version string

### 1.5.2

-   lowering the max message length before something is put into an file embed from 2000 (discord max) to 800.

### 1.5.3

-   add handling for deleted channels inside profile

### 1.5.4

-   improve config change on karma keywords with handling whitespaces and such

### 1.6.0

-   add thumps down automatically

### 1.6.1

-   fix profile changes

### 1.6.2

-   fix bugged logging of karma thanks
-   fix config panel bug

### 1.6.3

-   fix edit bug

### 1.7.0

-   refactoring code
-   various small changes (info embed uptime, help & info embed color, etc.)

### 1.8.0

-   self deletion is configureable
-   emojis are configureable
-   change descriptions of config values in the help command

### 1.8.1

-   improve on config embed by iterating over the dict and filtering out the unchangeable keys

### 1.9.1

-   fix config values of length 1 to add config keys
-   add a tutor command that explains the karma system under the current configuration

### 1.10.0

-   add module load, unload, reload
-   add global leaderboard, add channel specific leaderboard
-   refactoring tutor descriptions and embeds
-   remove all reactions on click of removal reactione emoji

### 1.10.1

-   fixing karma_service pipeline

### 1.10.2

-   using converters instead of loops and fixing channel leaderboards

### 1.10.3

-   catch exception for converter

### 1.10.4

-   another fix for channel leaderboards

### 1.10.5

-   another fix for channel leaderboards

### 1.10.6

-   another fix for channel leaderboards

### 1.11.0

-   creating a timed leaderboard of global or channel

### 1.11.1

-   fix leaderboard help command

### 1.11.2

-   fix profile bug

### 1.11.3

-   fix profile bug

### 1.11.4

-   fix edit tracking bug introduced by timestamp

### 1.12.0

-   apply local role hierarchy to reduce and block commands
-   add owner config property
-   add docs string to everything
-   add config file to git ignore, add example file.

### 1.13.1

-   fix config embed
-   fix config insertions that were bugged due to wrong predicate
-   add config response to keys that do not exist
-   remove reactions on message edit for invalid karma messages
-   change tutor text slightly

### 1.13.2

-   fix profile bug

### 1.14.0

-   removed cooldowns also now remove active cooldowns

### 1.15.0

-   changeable permissions
-   latency in info embed
-   change reactions / explain on partial edit

### 1.16.0

-   filter out greentext thanks from aura
-   improve emoji deletion on click:
    -   delete other emojis other than karma_gain when it is clicked
    -   delete only aura emojis

### 1.16.1

-   improve latency by not rounding, thus latency being exact.

### 1.16.2

-   fix greentext

### 1.17.0

-   added pipenv
-   added flake8 and black configuration files

### planned features

-   check the validity of the data returned from the database
-   complete partial edit tracking
-   remove cooldown on karma removal
-   track message edits with changed mentions
-   add sentiment analysis or other NLP stuff.
-   rework python models and mongodb queries, should not change anything about the api.
-   add tests for every major functionality that does require mocking the discord library
