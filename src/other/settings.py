import os, dotenv, sys


def find_config():
    dotenv.load_dotenv(dotenv.find_dotenv())
    URI = os.environ.get("URI")
    AURA_PASSWD = os.environ.get("AURA_PASSWD")
    USER = os.environ.get("USER")
    return (URI, (USER, AURA_PASSWD))
