from neo4j import GraphDatabase
import sys
import os
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
            raise SystemError(
                "No credentials found, checks .env or platform ENVS")
        try:
            (URI, AUTH) = creds
            self.driver = GraphDatabase.driver(URI, auth=AUTH)
        except ConnectionError:
            print(
                "Couldn't connect, check if connection variables are correct and internet connection"
            )

    def get_departments(self, id, name, count, sort):
        params = []
        if isinstance(id, int) or (isinstance(id, str) and id.isdecimal()):
            params.append(f"id:{id}")
        if isinstance(name, str) and len(name) > 0:
            params.append(f"name:'{name}'")
        params_str = "{" + ",".join(params) + "}"
        if sort is None:
            sort = ""
        elif sort not in ['name', 'id', 'count', 'name DESC', 'id DESC', 'count DESC']:
            return Exception({"message": "sort property is supposed to be field of :Department or count property"})
        else:
            if sort not in ['count', 'count DESC']:
                sort = f"d.{sort}"
            sort = f"ORDER BY {sort}"
        if count is None:
            count = ""
        elif not isinstance(count, int) or (isinstance(count, str) and count.isdigit()):
            return Exception({"message": "Count is supposed to be a number!"})
        else:
            if isinstance(count, str):
                count = int(count)
            count = f"WHERE count = {count}"
        deps, summary, keys = self.driver.execute_query(
            queries["GET_DEPARTMENTS"].replace("$params", params_str).replace("$sort", sort).replace("$count", count))
        results = [record.data() for record in deps]
        return results

    def get_employee_info(self, id):
        try:
            records, summary, keys = self.driver.execute_query(
                queries["GET_EMP_INFO"], parameters_={"id": id})

            return [record.data() for record in records]
        except Exception as e:
            return e

    def get_subordinates(self, id):
        try:
            records, summary, keys = self.driver.execute_query(
                queries["GET_SUBORDINATES"], parameters_={"id": id})
            return [record.data() for record in records]
        except Exception as e:
            return e

    def put_employee(self, id, name, last_name, position, department):
        try:
            parameters = {}
            if id:
                parameters["id"] = id
            if name:
                parameters["name"] = name
            if last_name:
                parameters["last_name"] = last_name
            if position:
                parameters["position"] = position
            if department:
                parameters["department"] = department
            if len(parameters) != 5:
                return "Please insert all of the arguments"
            records, summary, keys = self.driver.execute_query(
                queries["SET_EMPLOYEE_BY_ID"], parameters_=parameters
            )
            results = []
            for record in records:
                results.append(record.data())
            if len(results) == 0:
                return "Couldn't find employee with such ID"
            return results
        except Exception as e:
            return e

    def get_employees(self, name, last_name, position, sort):
        try:
            params = []
            if name:
                params.append(f"name:'{name}'")
            if last_name:
                params.append(f"last_name:'{last_name}'")
            if position:
                params.append(f"position:'{position}'")
            newSort = ""
            match sort:
                case "name":
                    newSort = ".name"
                case "last_name":
                    newSort = ".last_name"
                case "position":
                    newSort = ".position"
                case _:
                    pass
            query_params = "{" + ",".join(params) + "}"
            records, summary, keys = self.driver.execute_query(
                queries["GET_EMPLOYEES"]
                .replace("$params", query_params)
                .replace("$sort", newSort)
            )
            results = []
            for record in records:
                results.append(record.data())
            return results
        except Exception as e:
            return e

    def get_employees_by_department_id(self, id):
        try:

            records, summary, keys = self.driver.execute_query(
                queries["GET_EMP_BY_DEP"].replace("$relation", "WORKS_IN"),
                parameters_={"id": id},
            )
            match len(records):
                case 0:
                    return []
                case _:
                    results = [record.data() for record in records]
                    return results

        except Exception as e:
            return e

    def delete_employee(self, emp_id):
        try:
            emp_result, emp_summary, _ = self.driver.execute_query(
                queries["DELETE_EMP"], parameters_={"id": emp_id}
            )

            if emp_summary.counters.nodes_deleted == 0:
                return "No employee found for deletion."

            if not emp_result:
                return "Could not find employee ERROR!!"

            dep_id = emp_result[0].data()
            managers_result, _, _ = self.driver.execute_query(
                queries["GET_MANAGER"], parameters_={"id": dep_id["id"]}
            )
            emp_count_result, _, _ = self.driver.execute_query(
                queries["GET_EMP_BY_DEP"].replace("$relation", "WORKS_IN"),
                parameters_={"id": dep_id["id"]},
            )
            if len(managers_result) == 0 and len(emp_count_result) != 0:
                employee_to_promote_id = emp_count_result[0].data()["e"]
                promotion_result, _, _ = self.driver.execute_query(
                    queries["PROMOTE_EMP"],
                    parameters_={
                        "emp_id": employee_to_promote_id["id"],
                        "dep_id": dep_id["id"],
                    },
                )

                if promotion_result:
                    prom = self.driver.execute_query(
                        queries["PROMOTE_EMP2"].replace(
                            "$manager_id", f"{employee_to_promote_id["id"]}"
                        ),
                        parameters_={
                            "emp_id": employee_to_promote_id["id"],
                            "dep_id": dep_id["id"],
                        },
                    )
                    if prom:
                        return f"{promotion_result[0].data()} has become the new manager of department {dep_id}"
                    else:

                        return "Error promoting employee to manager."

                else:

                    return "Error promoting employee to manager."

            return "Successfully deleted Employee."

        except Exception as e:
            return str(e)

    def add_employee(self, name, last_name, position, department):
        try:
            full_name = "{" + f"name:'{name}', last_name:'{last_name}'" + "}"
            records, summary, keys = self.driver.execute_query(
                queries["GET_EMPLOYEES"]
                .replace("$sort", "")
                .replace("$params", full_name)
            )
            if len(records) > 0:
                return "Name is not UNIQUE!"
            parameters = {
                "name": name,
                "last_name": last_name,
                "position": position,
                "department": department,
            }
            records, summary, keys = self.driver.execute_query(
                queries["CREATE_EMP_TO_DEP"].replace("$relation", "WORKS_IN"),
                parameters_=parameters,
            )
            if len(records) == 0:
                return "Nie utworzono!"
            results = []
            for record in records:
                results.append(record.data())
            return results
        except Exception as e:
            return e

    def create_employees(self):
        try:
            done_departments = []
            for employee in employees:
                self.driver.execute_query(
                    queries["CREATE_EMP_TO_DEP"].replace(
                        "$relation", "WORKS_IN"),
                    parameters_=employee,
                )

                if employee["department"] not in done_departments:
                    done_departments.append(employee["department"])
                    for colleague in employees:
                        if employee != colleague:
                            if employee["department"] == colleague["department"]:
                                self.driver.execute_query(
                                    queries["EMP_TO_EMP"].replace(
                                        "$relation", "MANAGES"
                                    ),
                                    parameters_={
                                        **employee,
                                        "name2": colleague["name"],
                                        "last_name2": colleague["last_name"],
                                        "position2": colleague["position"],
                                    },
                                )
                        # self.driver.execute_query(queries["ADD_BOSS"], parameters_={**employee})

                        self.driver.execute_query(
                            queries["CREATE_EMP_TO_DEP"].replace(
                                "$relation", "MANAGES"
                            ),
                            parameters_=employee,
                        )
            return True

        except Exception as e:
            print(e)
            return False

    def close(self):
        self.driver.close()

    def drop_db(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
