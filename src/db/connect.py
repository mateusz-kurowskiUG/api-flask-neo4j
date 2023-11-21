from neo4j import GraphDatabase
import sys, os
from ..other.settings import find_config
import asyncio


class Db:
    def __init__(self):
        creds = find_config()
        if not all(var is not None for var in creds):
            print("ERROR!")
            raise SystemError("No credentials found, checks .env or platform ENVS")
        try:
            (URI, AURA_PASSWD, USER) = creds
            self.driver = GraphDatabase.driver(URI, auth=(USER, AURA_PASSWD))
        except ConnectionError:
            print(
                "Couldn't connect, check if connection variables are correct and internet connection"
            )

    def create_db(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            
            session.close()


db = Db()
db.create_db()
db.driver.close()
