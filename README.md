# api-flask-neo4j

API with Flask and Neo4j

1. Remember to set project's interpeter to poetry's venv
1. Project uses Poetry, to run commands always use `poetry run` e.g
   `poetry run python main.py`

1. To run server:
   `poetry run flask --debug --app src.api.api_main run`

Dokumentacja:

3. GET /employees
   optional params:
   name
   last_name
   postition
   sort = name of the field e.g name || last_name || position

4 POST /employees
body:{
name
last_name
position
department
}

5. PUT /employees/:id
   all required!
   body:{
   name
   last_name
   position
   department
   }

6.DELETE /employees/:id
nothing to pass

7.GET /employees/:id/subordinates
nothing to pass

8. GET /employees/:id
   nothing to pass
   returns:
   name_of_manager, last_name_of_manager, name_of_department, no_employees_of_department

9.get /departments
optional:
{
id=number
name=string
sort= (name || id || count) + DESC e.g sort="name DESC" or sort="count"
count= number
} 10. get /departments/:id/employees
