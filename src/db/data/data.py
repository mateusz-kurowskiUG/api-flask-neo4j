import json

queries = {
    "CREATE_EMPLOYEE_IF_NE": "MERGE (e:Employee {name:$emp_name, position:$position})",
    "CREATE_DEPARTMENT_IF_NE": "MERGE (d:Department {name:$dep_name})",
    "CREATE_EMP_TO_DEP": """ MERGE (e:Employee {name:$emp_name, position:$position})
    MERGE (d:Department {name:$dep_name})
    MERGE (e)-[{r:$relation} ]->(d)
    return e,r,d""",
    "CREATE_DEP_TO_EMP": "MERGE (d:Department {name:$dep_name})",
}


def find_data():
    with open("./MOCK_DATA.json") as file:
        data = json.load(file)
        return data


employees = find_data()
