import requests
import psycopg2
import json

connection = psycopg2.connect(host="localhost", dbname="SOEN-363-Project", user="postgres", password="1234", port=5432)
cursor = connection.cursor()