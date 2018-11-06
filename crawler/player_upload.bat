@echo off
setlocal enabledelayedexpansion
SET /P uname="MongoDB user name: "
SET /P pass="MongoDB password: "
cd .\player_jsons
dir /a:d /b > ../dirnames.txt 2>&1
cd ..
for /f "tokens=*" %%B in (dirnames.txt) do (
dir .\player_jsons\%%B /b > .\player_jsons\filenames.txt 2>&1
for /f "tokens=*" %%A in (.\player_jsons\filenames.txt) do mongoimport --host mongodb+srv://nsp-cluster-zqniz.mongodb.net/test --ssl --username %uname% --password %pass% --authenticationDatabase admin --db Players --collection %%B --type JSON --file player_jsons\%%B\%%A
del .\player_jsons\filenames.txt
)
del dirnames.txt