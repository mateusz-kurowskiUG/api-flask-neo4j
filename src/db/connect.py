from neo4j import GraphDatabase
import sys, os
from ..other.settings import find_config
import asyncio
from src.db.data.create import (
    queries,
    example_data,
    positions,
    positions_with_departments,
)
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
            (URI, AURA_PASSWD, USER) = creds
            self.driver = GraphDatabase.driver(URI, auth=(USER, AURA_PASSWD))
        except ConnectionError:
            print(
                "Couldn't connect, check if connection variables are correct and internet connection"
            )

    def create_employees(self):
        with self.driver.session() as session:
            for employee, role in zip(
                example_data["employees"], positions_with_departments
            ):
                position, department = role
                # print(employee, role)
                query_employee = (
                    queries["create_employee"]
                    .replace("$name", f"'{employee}'")
                    .replace("$position", f"'{position}'")
                )
                session.run(query=query_employee)

                query_department = queries["create_department"].replace(
                    "$name", f"'{department}'"
                )

    def drop_db(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
