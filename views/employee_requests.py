import sqlite3
import json
from models import Employee, Location
EMPLOYEES = [
    {"id": 1, "name": "James Baxter"},
    {"id": 2, "name": "Raquel Roberts"},
    {"id": 3, "name": "Johnny James"}
]

def get_all_employees():
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.location_id,
            l.name location_name,
            l.address location_address
        FROM Employee e
        JOIN Location l
            ON l.id = e.location_id
        """)
        employees = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            employee = Employee(row['id'], row['name'], row['location_id'])
            location = Location(
            row['location_id'], row['location_name'], row['location_address'])
            employee.location = location.__dict__
            employees.append(employee.__dict__)
    return employees


def get_single_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            e.id,
            e.name
        FROM employee e
        WHERE e.id = ?
        """, ( id, ))
        data = db_cursor.fetchone()
        employee = Employee(data['id'], data['name'], data['location_id'])
        return employee.__dict__
    
def get_employees_by_location(location_id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.name
        from Employee e
        where e.location_id = ?
        """, ( location_id, ))

def create_employee(employee):
    max_id = EMPLOYEES[-1]["id"]
    new_id = max_id + 1
    employee["id"] = new_id
    EMPLOYEES.append(employee)
    return employee

def delete_employee(id):
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            EMPLOYEES.pop(index)
            break

def update_employee(id, new_employee):
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            EMPLOYEES[index]["name"] = new_employee["name"]
            break
