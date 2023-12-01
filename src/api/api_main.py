from flask import Flask, request, jsonify
from src.db.connect import Db
import json
from flasgger import Swagger

db = Db()
# db.drop_db()
# is_created = db.create_employees()
app = Flask(__name__)
swagger = Swagger(app)


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
def get_subordinates(id):
    if not isinstance(id, int):
        if isinstance(id, str) and id.isdecimal():
            id = int(id)
        else:
            return "ID IS SUPPOSED TO BE INTEGER!", 403

    result = db.get_subordinates(id)

    if isinstance(result, Exception):
        return result, 500

    return jsonify(result), 200


@app.post("/employees")
def post_employees():
    json_data = request.json

    name = json_data.get("name")
    last_name = json_data.get("last_name")
    position = json_data.get("position")
    department = json_data.get("department")
    if not name or not last_name or not position or not department:
        return "All of the arguments must be given!", 403

    result = db.add_employee(name, last_name, position, department)
    if isinstance(result, str):
        return result, 403
    return result, 200


@app.get("/employees/<id>")
def get_employee_info(id):
    if not isinstance(id, int):
        if isinstance(id, str) and id.isdecimal():
            id = int(id)
        else:
            return "ID IS SUPPOSED TO BE INTEGER!", 403

    result = db.get_employee_info(id)

    if isinstance(result, Exception):
        return result, 500

    return jsonify(result), 200


@app.put("/employees/<id>")
def put_employee(id):
    if id is None or "":
        return "No ID provided!", 404
    try:
        int_id = int(id)
    except Exception as e:
        return e, 403

    json_data = request.json
    name = json_data.get("name")
    last_name = json_data.get("last_name")
    position = json_data.get("position")
    department = json_data.get("department")
    if not name or not last_name or not position or not department:
        return "All of the arguments must be given!", 404

    result = db.put_employee(int_id, name, last_name, position, department)
    if isinstance(result, Exception):
        return str(result), 403
    if isinstance(result, str):
        return result, 404
    return result, 200


@app.delete("/employees/<id>")
def delete_employee(id):
    if not id or not id.isdigit():
        return ({"message": "ID is supposed to be INTEGER"}), 403
    result = db.delete_employee(int(id))

    if isinstance(result, Exception):
        return jsonify(result), 500
    return jsonify(result), 200


@app.get("/departments")
def get_departments():
    dep_id = request.json.get("id")
    name = request.json.get("name")
    count = request.json.get("count")
    sort = request.json.get("sort")
    result = db.get_departments(dep_id, name, count, sort)
    if isinstance(result, Exception):
        return jsonify(result.args), 500
    if result is not None:
        return json.dumps(result), 200
    return "Error", 404


@app.get("/departments/<id>/employees")
def get_employees_departments(id):
    if not id or not id.isdigit():
        return ({"message": "ID is supposed to be INTEGER"}), 403
    result = db.get_employees_by_department_id(int(id))
    if isinstance(result, Exception):
        return jsonify(result), 500
    if isinstance(result, str):
        return jsonify(result), 404
    if isinstance(result, list):
        if len(result) == 0:
            return "Couldn't find such an employee", 404
        return jsonify(result), 200
    return jsonify(result), 500
