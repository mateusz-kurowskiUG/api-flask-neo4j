queries = {
    "create_employee": "CREATE (e:Employee)",
    "create_department": "CREATE (d:Department)",
    "employee_works_in_department": "MATCH (n:employee $name),(d:Department $department)",
    "employee_manages_department": "",
    "employee_manages_employee": "",
}

example_data = {"employees": [], "departments": []}
