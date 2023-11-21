from neo4j import *



class Connect:
    def __init__(self):
        self.driver = GraphDatabase.driver()