import requests
import psycopg2

connection = psycopg2.connect(host = "localhost", dbname ="SOEN-363-Project", user="postgres", password ="1234", port = 5432)
cursor = connection.cursor()

stmHeaders = {
    "accept": "application/json",
    "apiKey": "l78e91cc66e0c54b5cbddbf53eefc45120"
}

stmUrl = "https://api.stm.info/pub/od/i3/v1/messages/etatservice"


stmResponse = requests.get(stmUrl, headers=stmHeaders).json()
print(stmResponse)
