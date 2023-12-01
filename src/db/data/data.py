import json

queries = {
    "CONSTRAINT": "CREATE CONSTRAINT ON (n:player) ASSERT n.id IS UNIQUE",
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
    MATCH(e:Employee {id:$id}) -[pr]->(d:Department)
    MERGE (d2:Department {name:$department})
    SET e.name = $name, e.last_name = $last_name,
    e.position = $position
    MERGE (e)-[r:WORKS_IN]->(d2)
    DELETE pr
    return e
    """,
    "DELETE_EMP": """
    MATCH (e:Employee {id:$id})-[r]->(d:Department)
    DETACH DELETE e
    return d.id as id
    """,
    "GET_EMP_BY_DEP": """
    MATCH (e:Employee)-[r:$relation]->(d:Department {id:$id})
    return e
    """,
    "GET_SUBORDINATES": """
    MATCH (e:Employee {id:$id})-[r:MANAGES]->(e2:Employee)
    return e2
    """,
    "GET_MANAGER": """
    MATCH (e:Employee)-[r:MANAGES]->(d:Department {id:$id})
    return e
    """,
    "FIND_MANAGED_DEP": """
    MATCH (e:Employee)
    """,
    "CHOSE_NEW_MANAGER": """
    MATCH (e:Employee)-[r:WORKS_IN]->(d:Department)
    """,
    "DELETE_DEP": """
    MATCH (d:Department {id:$id})
    return d
    """,
    "GET_ONE_EMP_BY_DEP": """
    MATCH (e:Employee)-[r:WORKS_IN]->(d:Department{id:$id})
    return e.id
    limit 1
    """,
    "PROMOTE_EMP": """
    MATCH (e:Employee {id:$emp_id})-[r:WORKS_IN]->(d:Department {id:$dep_id})
    CREATE (e)-[r2:MANAGES]->(d)
    return e
    """,
    "PROMOTE_EMP2": """
    MATCH (e:Employee {id:$emp_id}), (e2:Employee)-[r:WORKS_IN]->(d:Department {id:$dep_id})
    WHERE e2.id <> $manager_id
    CREATE (e)-[r2:MANAGES]->(e2)
    return e
    """,
    "GET_DEP_ID_BY_EMP": """
    MATCH (e:Employee)-[r]->(d:Department {id:$id})
    return d.id
    """,
    "GET_DEPARTMENTS": """
        MATCH (e:Employee)-[r]-> (d:Department $params)
        WITH d, count(e) AS count
        $count
        return d,count
        $sort
    """,
    "COUNT_EMP_BY_DEP": """
    MATCH (e:Employee)-[r:]->(d: {id:$id})
    WITH count(e) AS cnt
    WHERE cnt
    """,
    "GET_EMP_INFO": """
    MATCH (e:Employee {id:$id})-[r]->(d:Department)
    MATCH (e2:Employee)-[r2:WORKS_IN]->(d)
    MATCH (m:Employee)-[r3:MANAGES]->(d)
    WITH m,d,count(e2) as count
    return m.name as imie_managera, m.last_name as nazwisko_managera, d.name as nazwa_departamentu, count as liczba_pracownikow
    """
}


def find_data():
    with open("src\db\data\MOCK_DATA.json") as file:
        data = json.load(file)
        return data


employees = find_data()
