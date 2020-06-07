## Version History
### 0.1.0
* Give [karma category type] command implemented (**done**)
* Configuration.yaml created and filled (**done**)
* User feedback for correct usage of the [give karma] command (**done**)
* User feedback for incorrect usage of the [give karma] command (**done**)
* Filtering role mentions (**done**)
* Filtering messages with more than one mention (**done**)
* Filtering messages without a user mention, this includes everyone and here mentions. (**done**)
* Bot can be started through Docker. (**done**)

### 0.2.0
* Docker-compose setup with database complete with database 
dashboard, mongodb and discord bot. (**done**)
* Leaderboard : get single of type implemented (**done**)
* Leaderboard : get top x of type implemented (**done**)
* Karma Service: upsert implemented (**done**)
* Karma Service: get implemented (**done**)
* Karma Service: filter top x of karma type implemented (**done**)
* Karma cooldown user after executing give [karma category type] successfully (**done**)
* Filtering other bot mentions (**done**)

### 0.3.0
* retrieve database configuration from config.yaml (**done**)
* centralize configuration into its own class (**done**)
* get karma [karma_type] returns karma for message author (**done**)

### 0.4.0
* add command to reset karma of member (all in guild) (**done**)
* add command to reset karma of member (type in guild) (**done**)
* add role configuration to the bot (**done**)

### 0.5.0
* modify get karma command to be executed with the respective category command without introducing a separate command (**done**)
* first version of a README.md (**done**)
* added contributor.MD (**done**)

### 0.6.0 rework version
* remove karma category commands (**done**)
* detect karma by thanks @user and variations (**done**)
* remove leaderboard functionality (**done**)
* remove karma type from service and model classes (**done**)
* add channel_id to model classes and services (**done**)
* add commands to change the configuration on the fly (**done**)
* aggregate karma on karma without any arguments (**done**)
* remove karma on message delete (**done**)
* log karma in specific channel (**done**)

### 0.7.0 profiles
* update documentation (**done**)
* convert config into module level variable / methods (**done**)
* blacklist / whitelist members (**done**)
* add karma profile embed (member.name+#+member.discriminator, top x karma channels + karma for each) (**done**)
* move guild out of config and get it from the message (**done**)
* add help command back in and add default descriptions (**done**)
* add profile picture to profile embed (**done**)
* various profile embed improvements (proper spacing etc.) (**done**)

### 0.8.0 blacklist dm
* dm users that are blacklisted when they try to give out karma (**done**)
* improve config command:
    - check for non existent configuration parameters (**done**)
    - filter out certain configuration parameters (prefix and token) (**done**)

### 0.9.0 small reworks, config embed, configuration changes, reactions, tests, logging, error
* add some exception handling (**done**)
* add logging to aura (**done**)
* add config embed (**done**)
* make sure aura works only inside of guilds by adding guild checks (**done**)
* make it possible to thank several people in a message (**done**)
* make it possible to get the karma of several mentions in a message (**done**)
* add check on nickname for profile (**done**)
* add nickname to profile (**done**)
* add emote thumps up to thanks messages (**done**)
* add config in regards to show how karma was received (**done**)
* add tests for every major functionality that does not require mocking the discord library (**done**)
* refactor core model classes (**done**)

### 0.9.1
* fix karma give not working (**done**)

### 1.0.0 release version
* tidy up code (**done**)

### 1.1.0 config and help command
* rework help command (**done**)
* change some config command values (**done**)
* add prefix and mention of bot for commands (**done**)

### 1.1.1
* hotfix reset command (**done**)

### 1.1.2
* hotfix double karma bug (**done**)

### 1.1.3
* hotfix karma mention (**done**)

### 1.1.4
* hotfix message author karma thanks (**done**)

### 1.1.5
* fix logging (**done**)
* fix profile and karma messages with bot mention and id usage (**done**)
* fix blacklist, whitelist, reset with bot mention and id usage (**done**)

### 1.1.6
* fix reset method AGAIN (**done**)

### 1.1.7
* let conversion return a set of members to prevent spamming (**done**)

### 1.1.8
* fix multiple karma thanks filter out duplicates (**done**)

### 1.1.9
* add message link to log messages of karma gain (**done**)

### 1.1.10
* fix profile not working with args (**done**)

### 1.1.11
* fix profile taking not only the first user arg (**done**)

### 1.2.0 embed and reaction removal event
* add information embed on @mention of bot (**done**)
* remove karma on removing the reaction (**done**)

### 1.2.1
* fix karma on message deletion not working correctly (**done**)

### 1.3.0 cooldown, thank you keywords configureable
* thank you keyword list configureable (**done**)
* cooldown based on giver-receiver instead of only giver (**done**)
* log karma deletes into the log as well (**done**)

### 1.3.1
* fix message delete await validate message (**done**)
* fix version string in info embed (**done**)

### 1.4.0
* rework config menu (**done**)
* make deletion logging more consistent (**done**)
* add config help command (**done**)

### 1.4.1
* fix some help config descriptions (**done**)

### 1.4.2
* fix version string in info embed (**done**)

### 1.4.3
* fix config help embed formatting (**done**)

### 1.4.4
* fix version string in info embed (**done**)

### 1.5.0
* filter out messages where the thanks is inside of " " (**done**)
* track partial message edits (**done**)
* add ways for normal members to revoke karma given out (**done**)
* fix profile embed spacing (**done**)
* fix config embed spacing (**done**)
* add command to view all blacklisted members (**done**)

### 1.5.1
* again version string (**done**)

### 1.5.2
* lowering the max message length before something is put into an file embed from 2000 (discord max) to 800. (**done**)

### 1.5.3
* add handling for deleted channels inside profile (**done**)

### 1.5.4
* improve config change on karma keywords with handling whitespaces and such (**done**)

### 1.6.0
* add thumps down automatically (**done**)

### 1.6.1
* fix profile changes (**done**)

### 1.6.2
* fix bugged logging of karma thanks (**done**)
* fix config panel bug (**done**)

### 1.6.3
* fix edit bug (**done**)

### 1.7.0
* refactoring code (**done**)
* various small changes (info embed uptime, help & info embed color, etc.) (**done**)

### 1.8.0
* self deletion is configureable (**done**)
* emojis are configureable (**done**)
* change descriptions of config values in the help command (**done**)

### 1.8.1
* improve on config embed by iterating over the dict and filtering out the unchangeable keys (**done**)

### 1.9.1
* fix config values of length 1 to add config keys (**done**)
* add a tutor command that explains the karma system under the current configuration (**done**)

### 1.10.0
* add module load, unload, reload (**done**)
* add global leaderboard, add channel specific leaderboard (**done**)
* refactoring tutor descriptions and embeds (**done**)
* remove all reactions on click of removal reactione emoji (**done**)

### 1.10.1
* fixing karma_service pipeline (**done**)

### 1.10.2
* using converters instead of loops and fixing channel leaderboards (**done**)

### 1.10.3
* catch exception for converter  (**done**)

### 1.10.4
* another fix for channel leaderboards (**done**)

### 1.10.5
* another fix for channel leaderboards (**done**)

### 1.10.6
* another fix for channel leaderboards (**done**)

### 1.11.0
* creating a timed leaderboard of global or channel (**done**)

### 1.x.0
* remove cooldown on karma removal
* track message edits with changed mentions

### 1.y.0
* rework python models and mongodb queries, should not change anything about the api.
* add tests for every major functionality that does require mocking the discord library