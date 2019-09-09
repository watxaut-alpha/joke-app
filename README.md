#Introduction
This project is the continuation of my other repository joke-automation-mail. 
Both projects are intended to send text to the user (in this case a joke) but this one is 
a little bit more complicated than sending just a mail no no. In this one I created a bot
that is able to send and make the user rate the joke. All the user input goes to a 
postgres DB and then analysed.

#Installation
You can try the project in either a Python Virtual Environment or in Docker (preferred option)

## Python Virtual environment
Execute the following commands in order to create a Python Virtual Environment in the 
<your_dir>:
```bash
cd <your_dir>
pip3 install virtualenv
virtualenv venv --python=python3.6
source venv/bin/activate
```
Note: this works for MacOS and Linux, for windows see how to activate Virtual Environments

## src/bot/secret.py
In here you have to define your Telegram bot token (first you will need to create a bot 
asking the BotFather in Telegram):
```python
# src/bot/secret.py
token = "Your Telegram bot token here"
```

## src/db/secret.py
In here you will have to define your connection to the DB:
```python
POSTGRES_USER = 'your user name'
POSTGRES_PASSWORD = 'your pwd for the user'

host = 'the host of the DB (localhost or other)'
s_db_name = 'the DB schema name'  
```

#Incoming next steps
* Add a BI client or a Jupyter Notebook in order to visualise the ratings of the jokes
* Add scrappers looking for jokes and make a functionality in the bot to validate 
these new jokes
* Segment users in different categories depending on their affinity with the jokes 
