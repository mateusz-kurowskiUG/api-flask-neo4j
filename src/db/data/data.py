import json

queries = {
    "CREATE_EMP_TO_DEP": """
    MERGE (e:Employee {name:$name, last_name:$last_name, position:$position})
    MERGE (d:Department {name:$department})
    MERGE (e)-[r:$relation ]->(d)
    SET e.id = id(e), d.id = id(d)
    return e,r,d
    """,
    "EMP_TO_EMP": """
    MERGE (e1:Employee {name:$name, last_name:$last_name, position: $position})
    MERGE (e2:Employee {name:$name2, last_name:$last_name2, position: $position2})
    MERGE (e1)-[r:$relation]->(e2)
    SET e1.id = id(e1), e2.id = id(e2)
    return e1,r,e2
    """,
    # "ADD_BOSS": "MERGE (p {name:'Alan', last_name:'Key', position:'President'})-[r:MANAGES]->(e:Employee {name:$name, last_name:$last_name, position:$position})",
    "GET_EMPLOYEES": """
    MATCH (e:Employee $params)
    return e
    ORDER BY e$sort
    """,
    "SET_EMPLOYEE_BY_ID": """
    MATCH(e:Employee {id:$id})
    MERGE (d:Department {name:$department})
    SET e.name = $name, e.last_name = $last_name,
    e.position = $position
    MERGE (e)-[r:WORKS_IN]->(d)
    return e
    """,
}


def find_data():
    with open("src\db\data\MOCK_DATA.json") as file:
        data = json.load(file)
        return data


employees = find_data()
