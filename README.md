# SOEN-363
Team name: SubwaySurfers <br>
Team lead: [Keshan Kathiripilay](https://github.com/katkes) <br>
Team members:
- [Annabel Zecchel](https://github.com/annabelzecchel)
- [Tahsin Islam](https://github.com/Tahsin-Islam)
- [Midhurshaan Nadarajah](https://github.com/midhurshaan)

## Topic
Comparing and contrasting Montréal and New York City's public transit systems. 

## Overview
This project fetches data from the STM (Montréal public transit system) and MTA (New York City public transit system) API and stores it. The data includes service status messages, route information and trip updates. The fetched data is saved as JSON files for further analysis or usage.

## APIs used
- [STM](https://www.stm.info/en/about/developers)
- [Ville de Montreal](https://donnees.montreal.ca/dataset/?q=&sort=views_recent+desc&organization=societe-de-transport-de-montreal)
- [TTC](https://myttc.ca/developers)
- [MTA](https://new.mta.info/developers)

## Features
- Fetches service status messages and trip updates from the STM API.
- Parses Protobuf data from the STM API trip updates and converts it to JSON.
- Saves the fetched data as JSON files.

## Dependencies
The project requires the following dependencies:
- `requests`: For making HTTP requests to the STM API.
- `psycopg2`: For connecting to a PostgreSQL database.
- `protobuf`: For parsing Protobuf data.
- `google.protobuf.json_format`: For converting Protobuf messages to JSON.
- `neo4j`: For connecting to a Neo4j database.

## Report
[Docs Link](https://docs.google.com/document/d/1iI6DHH9BiiiCHJ30YzzL8wDj_BObIsEIM19i_BdAHso/edit?usp=sharing)

## Slides Presentation
[Canva Link](https://drive.google.com/file/d/1aQMF_u0o4uyx1dbrHyfzhERl8ji97Icv/view?usp=sharing)

