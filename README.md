# Joke-app
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
----
This project is the continuation of my other repository 
[joke-automation-mail](https://github.com/watxaut-alpha/joke-mail-automation "jokes in mails yay"). 
Both projects are intended to send jokes to the user (in this case a joke) but this one is 
a little bit more complex than sending just a mail, hm hm no no no. 

![He knows it's not the same](resources/hmhm.gif)

This one adds a bunch of new stuff:
* An API (Fastapi - Python): CRUD for jokes, rating for jokes and joke validation
    * Postgresql DB
    * pgAdmin
* An HTML exported Jupyter Notebook with joke statistics ([here](https://watxaut.com/notebooks/ratings "Ratings Notebook")) 
* A Telegram Bot, as a fast interface for the API
* A Twitter bot that goes tweeting jokes
* Airflow: not really necessary for this low volume of tasks, but hey: when real ETL comes, you will be prepared
* "Docker this, Docker that": everything wrapped up with Docker Compose files

# Installation
* First you will need Docker installed
* Second, you will have to fill some Environment parameters
### config/env-airflow.env
* FERNET_KEY
You will need to run the following scrip to find the Fernet key for your host:
```bash
docker run puckel/docker-airflow:1.10.7 python -c "from cryptography.fernet import Fernet; FERNET_KEY = Fernet.generate_key().decode(); print(FERNET_KEY)"
```
### config/env-api.env
* JWT_SECRET_KEY (run 'openssl rand -hex 32' to get it)
* ALGORITHM (I use 'HS256')
* DOCS_USER (for the API Docs page)
* DOCS_PASSWORD (for the API Docs page)

### config/env-pgadmin.env
PGADMIN_LISTEN_PORT (normally you would use 555)
PGADMIN_DEFAULT_EMAIL (your user email)
PGADMIN_DEFAULT_PASSWORD (run 'openssl rand -hex 32' to get it)

### config/env-postgres.env
POSTGRES_SERVER=db (should be the name of the docker service for the postgres jokes db)
POSTGRES_USER (normally you would use 'postgres' as the usual non-safe choice)
POSTGRES_PASSWORD (run 'openssl rand -hex 32' to get it)

### config/env-telegram.dev.env and config/env-telegram.prod.env
TOKEN (you will get it from the Bot-father)
Chech this in order to [create a bot asking the BotFather 
in Telegram](https://core.telegram.org/bots#3-how-do-i-create-a-bot "A bot for creating bots")

### .env (at the root of your DEV environment)
Should look like this plus the environment variables you might have
```bash
COMPOSE_PATH_SEPARATOR=:
COMPOSE_FILE=docker-compose.dev.api.yml:docker-compose.dev.airflow.yml:docker-compose.dev.bot.yml
```

### .env (at the root of your PROD environment)
Should look like this plus the environment variables you might have
```bash
COMPOSE_PATH_SEPARATOR=:
COMPOSE_FILE=docker-compose.prod.api.yml:docker-compose.prod.airflow.yml:docker-compose.prod.bot.yml
```

## Scrappers
The community is giving feedback with more jokes from users, but I got a base of jokes from scrappers. But not every 
thing that is scrapped is a joke, it needs validation first. This is why the bot has the option "validate_joke",
which asks the user if the sent joke is actually a joke or not.

### Twitter
I call it scrapping, but I am just using the API wrapper library for Python: Tweepy, which
connects to Twitter via OAuth and returns tweets, although the idea is the same: get the
jokes automatically from a list of pages(users instead)

# Incoming next steps
* Add multi-language support
* Segment users in different categories depending on their affinity with the jokes 
