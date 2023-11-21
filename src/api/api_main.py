from flask import Flask, request

app = Flask(__name__)
print(__name__)


@app.get("/employees")
def get_employees():
    ...


@app.post("/employees")
def post_employees():
    ...


@app.put("/employees/<id>")
def put_employee(id):
    ...


@app.delete("/employees/<id>")
def delete_employee(id):
    ...


@app.get("/employees/<id>/subordinates")
def get_seubordinates(id):
    ...


@app.get("/departments")
def get_departments():
    ...


@app.get("/departments/:id/employees")
def get_employees_departments(id):
    ...
