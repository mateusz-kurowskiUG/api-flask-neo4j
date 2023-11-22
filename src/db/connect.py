from neo4j import GraphDatabase
import sys, os
from src.other.settings import find_config
import asyncio
import random
from src.db.data.data import employees, queries
import atexit

# defining function to run on shutdown
# def close_running_threads():
#     for thread in the_threads:
#         thread.join()
#     print "Threads complete, ready to finish"
# #Register the function to be called on exit
# atexit.register(close_running_threads)
# #start your process
# app.run()


class Db:
    def __init__(self):
        creds = find_config()
        if not all(var is not None for var in creds):
            print("ERROR!")
            raise SystemError("No credentials found, checks .env or platform ENVS")
        try:
            (URI, AUTH) = creds
            self.driver = GraphDatabase.driver(URI, auth=AUTH)
        except ConnectionError:
            print(
                "Couldn't connect, check if connection variables are correct and internet connection"
            )

    def create_employees(self):
        for employee in employees:
            self.driver.execute_query()

    def close(self):
        self.driver.close()

    def drop_db(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
