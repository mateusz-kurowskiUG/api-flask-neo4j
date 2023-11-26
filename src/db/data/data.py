import json

queries = {
    "CREATE_EMPLOYEE_IF_NE": "MERGE (e:Employee {name:$name,last_name:$last_name, position:$position})",
    "CREATE_DEPARTMENT_IF_NE": "MERGE (d:Department {name:$department})",
    "CREATE_EMP_TO_DEP": """
    MERGE (e:Employee {name:$name, last_name:$last_name, position:$position})
    MERGE (d:Department {name:$department})
    MERGE (e)-[r:$relation ]->(d)
    return e,r,d
    """,
    "CREATE_DEP_TO_EMP": "MERGE (d:Department {name:$department})",
    "EMP_TO_EMP": """
    MERGE (e1:Employee {name:$name, last_name:$last_name, position: $position})
    MERGE (e2:Employee {name:$name2, last_name:$last_name2, position: $position2})
    MERGE (e1)-[r:$relation]->(e2)
    return e1,r,e2
    """,
    "ADD_BOSS": "MERGE (p {name:'Alan', last_name:'Key', position:'President'})-[r:MANAGES]->(e:Employee {name:$name, last_name:$last_name, position:$position})",
    "GET_EMPLOYEES": """
    MATCH (e:Employee $params)
    return e
    ORDER BY e$sort
    """,
}


def find_data():
    with open("src\db\data\MOCK_DATA.json") as file:
        data = json.load(file)
        return data


employees = find_data()
