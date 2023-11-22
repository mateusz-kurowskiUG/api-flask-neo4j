queries = {
    "create_employee": "CREATE (e:Employee {name:$name,position:$position} ) return e",
    "create_department": "CREATE (d:Department {name:$name}) return d",
    "employee_works_in_department": "MATCH (e:Employee {name:$name}),(d:Department {name:$name}) CREATE (e)-[r:WORKS_IN]->(d) return e,r,d",
    "employee_manages_department": "MATCH (e:Employee {name:$name}),(d:Department {name:$name}) CREATE (e)-[r:MANAGES]->(d) return e,r,d",
    "employee_manages_employee": "MATCH (e1:Employee {name:$name}),(e2:Employee {name:$name}) CREATE (e1)-[r:MANAGES]->(e2) return e1,r,e2",
}

example_data = {
    "employees": [
        "Jan Kowalski",
        "Anna Nowak",
        "Krzysztof Wiśniewski",
        "Małgorzata Wójcik",
        "Piotr Kowalczyk",
        "Agnieszka Kamiński",
        "Andrzej Lewandowski",
        "Barbara Zieliński",
        "Michał Szymański",
        "Katarzyna Dąbrowski",
        "Tomasz Woźniak",
        "Joanna Kozłowski",
        "Paweł Jankowski",
        "Magdalena Mazur",
        "Marcin Wojciechowski",
        "Ewa Kwiatkowski",
        "Łukasz Krawczyk",
        "Kinga Kaczmarek",
        "Adam Piotrowski",
        "Natalia Grabowski",
        "Robert Zając",
        "Dorota Pawłowski",
        "Mateusz Michalski",
        "Patrycja Król",
        "Marek Wieczorek",
        "Aleksandra Jabłoński",
        "Jakub Nowicki",
        "Monika Witkowski",
        "Grzegorz Majewski",
    ],
    "departments": [
        "IT",
        "HR",
        "Finanse",
        "Marketing",
        "Helpdesk",
    ],
}
positions_it = [
    "Analityk systemowy",
    "Administrator sieci",
    "Specjalista ds. bezpieczeństwa IT",
    "Inżynier oprogramowania",
    "Architekt systemowy",
    "Specjalista ds. baz danych",
]
positions_hr = [
    "Specjalista ds. rekrutacji",
    "Specjalista ds. szkoleń",
    "HR Business Partner",
    "Analityk HR",
    "Doradca personalny",
    "Specjalista ds. rozwoju pracowników",
]
positions_finanse = [
    "Księgowy",
    "Analityk finansowy",
    "Specjalista ds. controllingu",
    "Auditor finansowy",
    "Kierownik działu finansowego",
    "Specjalista ds. faktur",
]
positions_marketing = [
    "Specjalista ds. marketingu internetowego",
    "Kierownik ds. komunikacji marketingowej",
    "Analityk rynku",
    "Copywriter",
    "Specjalista ds. social media",
    "Event Manager",
]
positions_helpdesk = [
    "Helpdesk Technician",
    "Support Specialist",
    "IT Service Desk Analyst",
    "Technical Support Engineer",
    "Customer Support Representative",
    "Admin",
]

# Połącz wszystkie positions w jedną listę
positions = [
    positions_it,
    positions_hr,
    positions_finanse,
    positions_marketing,
    positions_helpdesk,
]
positions_with_departments = []
for positionArray, department in zip(positions, example_data["departments"]):
    for position in positionArray:
        positions_with_departments.append((position, department))

# positions_with_departments = list(zip(example_data["employees"], positions))
