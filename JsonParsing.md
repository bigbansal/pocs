# I have used JQ https://stedolan.github.io/jq/ for processing of Json Data
yum install epel-release -y
yum update -y
yum install jq -y
   
# Once JQ is installed 

json_data='{"a":{"b":{"c":"d"}}}'

jq -n "$json_data" | jq .a # to see response in json format

jq -n "$json_data" | jq .a.b.c -r # to see in raw format

#If json is given in File Format

lets say => test.json

{
  "id": {
    "be": "295",
    "ts": "2283",
    "gok": 41,
    "ops": "N0483",
    "lis": "S"
  },
  "name": {
    "first": "G",
    "last": "B",
    "official_full": "G B"
  }
}

cat test.json | jq '.'

cat test.json | jq '.id'

cat test.json | jq '.name.first'
