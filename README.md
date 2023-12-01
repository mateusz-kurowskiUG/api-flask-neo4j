# api-flask-neo4j

API with Flask and Neo4j

1. Remember to set project's interpeter to poetry's venv
1. Project uses Poetry, to run commands always use `poetry run` e.g
   `poetry run python main.py`

1. To run server:
   `poetry run flask --debug --app src.api.api_main run`

Dokumentacja:

1. GET /employees
   optional params:
   name
   last_name
   postition
   sort = name of the field e.g name || last_name || position

2. POST /employees
   body:{
   name
   last_name
   position
   department
   }

3. PUT /employees/:id
   all required!
   body:{
   name
   last_name
   position
   department
   }

4.DELETE /employees/:id
nothing to pass

5. GET /employees/:id/subordinates
 nothing to pass

 6. get /departments
 optional:
 {
   name='dep_name'
   count=True
   sort=field e.g name
 }
 7. get /departments/:id/employees