from flask import Flask, request
from src.db.connect import Db

db = Db()
db.drop_db()
db.create_employees()
app = Flask(__name__)


@app.get("/employees")
def get_employees():
    return "f"


@app.get("/employees/<id>/subordinates")
def get_seubordinates(id):
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


@app.get("/departments")
def get_departments():
    ...


@app.get("/departments/:id/employees")
def get_employees_departments(id):
    ...
