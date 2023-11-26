from flask import Flask, request
from src.db.connect import Db
import json

db = Db()
db.drop_db()
db.create_employees()
app = Flask(__name__)


@app.get("/employees")
def get_employees():
    name = request.args.get("name")
    last_name = request.args.get("last_name")
    position = request.args.get("position")
    sort = request.args.get("sort")
    result = db.get_employees(name, last_name, position, sort)
    if result is not None:
        return json.dumps(result), 200
    return "Error", 404


@app.get("/employees/<id>/subordinates")
def get_seubordinates(id):
    ...


@app.post("/employees")
def post_employees():
    json_data = request.json

    name = json_data.get("name")
    last_name = json_data.get("last_name")
    position = json_data.get("position")
    department = json_data.get("department")
    if not name or not last_name or not position or not department:
        return "Podaj wszystkie argumenty!", 403

    result = db.add_employee(name, last_name, position, department)
    if isinstance(result, str):
        return result, 403
    return result, 200


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
