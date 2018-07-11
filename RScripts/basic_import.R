install.packages("rjson")
library("rjson")
json_data <- fromJSON(file="2007_10_30_RocketsAtLakers.json")
print(json_data)

