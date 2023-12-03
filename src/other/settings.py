import os
import dotenv


def find_config():
    dotenv.load_dotenv(dotenv.find_dotenv())
    URI = os.environ.get("URI")
    AURA_PASSWD = os.environ.get("AURA_PASSWD")
    NEO_USER = os.environ.get("NEO_USER")
    return (URI, (NEO_USER, AURA_PASSWD))
