@echo off
dir .\game_jsons /b > filenames.txt 2>&1
SET /P uname="MongoDB user name: "
SET /P pass="MongoDB password: "
echo %uname%
for /f "tokens=*" %%A in (filenames.txt) do mongoimport --host NSP-Cluster-shard-0/nsp-cluster-shard-00-00-zqniz.mongodb.net:27017,nsp-cluster-shard-00-01-zqniz.mongodb.net:27017,nsp-cluster-shard-00-02-zqniz.mongodb.net:27017 --ssl --username %uname% --password %pass% --authenticationDatabase admin --db NBA-Game-Data --collection Game-Records --type JSON --file game_jsons/%%A
del filenames.txt