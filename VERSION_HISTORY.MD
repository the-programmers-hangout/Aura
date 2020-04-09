## Version History
### 0.0.1
* Give [karma category type] command implemented (**done**)
* Configuration.yaml created and filled (**done**)
* User feedback for correct usage of the [give karma] command (**done**)
* User feedback for incorrect usage of the [give karma] command (**done**)
* Filtering role mentions (**done**)
* Filtering messages with more than one mention (**done**)
* Filtering messages without a user mention, this includes everyone and here mentions. (**done**)
* Bot can be started through Docker. (**done**)

### 0.0.2
* Docker-compose setup with database complete with database 
dashboard, mongodb and discord bot. (**done**)
* Leaderboard : get single of type implemented (**done**)
* Leaderboard : get top 25 of type implemented
* Karma Service: upsert implemented (**done**)
* Karma Service: get implemented (**done**)
* Karma Service: filter top x of karma type implemented
* Karma Service: cooldown user implemented
* Karma cooldown user after executing give [karma category type] successfully

### 0.0.3
* retrieve database configuration from config.yaml
* filter karma by channel, by channel category

### 0.0.4
* add setup command that is executed on first start (empty config.yaml)
* add commands to change the configuration on the fly