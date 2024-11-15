# SOEN-363
Team name: SubwaySurfers <br>
Team lead: [Keshan Kathiripilay](https://github.com/katkes) <br>
Team members:
- [Annabel Zecchel](https://github.com/annabelzecchel)
- [Tahsin Islam](https://github.com/Tahsin-Islam)
- [Midhurshaan Nadarajah](https://github.com/midhurshaan)

## Topic
Comparing and contrasting analytics with Montréal, Toronto and New York City's public transit systems. 

## Overview

This project fetches data from the STM (Montréal public transit), TTC (Toronto pubic transit), and MTA (New York City public transit) API and stores it. The data includes service status messages, route information and  and trip updates. The fetched data is saved as JSON files for further analysis or usage.

## Features
- Fetches service status messages and trip updates from the STM API.
- Parses Protobuf data from the STM API trip updates and converts it to JSON.
- Saves the fetched data as JSON files. [To be changed]

## Dependencies

The project requires the following dependencies:

- `requests`: For making HTTP requests to the STM API.
- `psycopg2`: For connecting to a PostgreSQL database.
- `protobuf`: For parsing Protobuf data.
- `google.protobuf.json_format`: For converting Protobuf messages to JSON.
