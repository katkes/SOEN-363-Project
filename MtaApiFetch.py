from HelperFunctions import fetch_and_create_json_mta_response_json, insert_into_mta_stop_line_tables
from Creds import connection

cursor = connection.cursor()

fetch_and_create_json_mta_response_json("ace")
fetch_and_create_json_mta_response_json("g")
fetch_and_create_json_mta_response_json("nqrw")
fetch_and_create_json_mta_response_json("")
fetch_and_create_json_mta_response_json("bdfm")
fetch_and_create_json_mta_response_json("jz")
fetch_and_create_json_mta_response_json("l")
fetch_and_create_json_mta_response_json("si")

insert_into_mta_stop_line_tables(cursor)