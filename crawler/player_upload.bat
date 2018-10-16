@echo off
setlocal enabledelayedexpansion
SET /P uname="MongoDB user name: "
SET /P pass="MongoDB password: "
echo %uname%
cd .\player_jsons
dir /a:d /b > ../dirnames.txt 2>&1
cd ..
for /f "tokens=*" %%B in (dirnames.txt) do (
dir .\player_jsons\%%B /b > .\player_jsons\filenames.txt 2>&1
for /f "tokens=*" %%A in (filenames.txt) do mongoimport --host NSP-Cluster-shard-0/nsp-cluster-shard-00-00-zqniz.mongodb.net:27017,nsp-cluster-shard-00-01-zqniz.mongodb.net:27017,nsp-cluster-shard-00-02-zqniz.mongodb.net:27017 --ssl --username %uname% --password %pass% --authenticationDatabase admin --db NBA-Game-Data --collection Game-Records --type JSON --file player_jsons\%%B\%%A
del .\player_jsons\filenames.txt
)
del dirnames.txt