# Joke-app
This project is the continuation of my other repository 
[joke-automation-mail](https://github.com/watxaut-alpha/joke-mail-automation "jokes in mails yay"). 
Both projects are intended to send jokes to the user (in this case a joke) but this one is 
a little bit more complex than sending just a mail, hm hm no no no. 
![He knows it's not the same](resources/hmhm.gif)

In this one I created a bot that is able to send a joke and make the user rate it. 
All the user input goes into a postgres DB and then is analysed.

# Installation
You can try the project in either a Python Virtual Environment or in Docker (preferred option)
BUT FIRST you need to define two files: bot.secret.py and db.secret.py files: 

### src/bot/secret.py
In here you have to define your Telegram bot token but first you will need to [create a bot 
asking the BotFather in Telegram](https://core.telegram.org/bots#3-how-do-i-create-a-bot "A bot for creating bots") if
you did not. Then the BotFather will give you the Bot's Token and you should put it in here like this:
```python
# src/bot/secret.py
token = "Your Telegram bot token here"
```

### src/db/secret.py
In here you will have to define your connection to the DB:
```python
POSTGRES_USER = 'your_db_user_name'
POSTGRES_PASSWORD = 'your_pwd_for_the_user'

host = 'the host of the DB (localhost or other)'
s_db_name = 'the DB schema name'  
```

## Method 1: Python Virtual environment
So if you want to install the repo localhost, this is the fastest way. Execute the following commands in order 
to create a Python Virtual Environment in <your_dir>:
```bash
cd <your_dir>
pip3 install virtualenv
virtualenv venv --python=python3.6
source venv/bin/activate
```
Note: this works for MacOS and Linux, for windows see how to install and activate Virtual 
Environments [here](https://virtualenv.pypa.io/en/latest/installation/).


## Method 2: Docker
If you want to run it in docker simply install docker (if you haven't) and build and run the container. 
I created a MakeFile for easier usage:
* "make build" in the root of the repo will build the container (needed if you changed the code)
* "make run" will run the container

# Incoming next steps
* Add a BI client or a Jupyter Notebook in order to visualise the ratings of the jokes
* Add scrappers looking for jokes and make a functionality in the bot to validate 
these new jokes
* Segment users in different categories depending on their affinity with the jokes 
