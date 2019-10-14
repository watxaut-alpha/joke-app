import requests
import random


def get_random_cat_fact():

    r = requests.get("https://cat-fact.herokuapp.com/facts/random/")
    if r:  # successful request 200
        fact = r.json()["text"]
    else:
        fact = None
    return fact


def get_random_number_fact():
    r = requests.get("http://numbersapi.com/random/trivia")
    if r:
        fact = r.text
    else:
        fact = None
    return fact


def get_random_fact():
    f = [get_random_cat_fact, get_random_number_fact]
    rand_num = random.randint(0, 1)
    print(rand_num)
    return f[rand_num]()
