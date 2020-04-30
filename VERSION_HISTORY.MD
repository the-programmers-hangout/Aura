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
* add karma profile embed

### 0.9.0
* filter get karma by channel
* add setup command that is executed on first start (empty config.yaml)
