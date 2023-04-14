employees = [
    {"id": 1, "name": "James Baxter"},
    {"id": 2, "name": "Raquel Roberts"},
    {"id": 3, "name": "Johnny James"}
]

def get_all_employees():
    return employees

def get_single_employee(id):
    for employee in employees:
        if employee["id"] == id:
            return employee
    return None

def create_employee(employee):
    max_id = max(employees, key=lambda x: x["id"])["id"]
    new_employee = {"id": max_id + 1, "name": employee["name"]}
    employees.append(new_employee)
    return new_employee

def delete_employee(id):
    for index, employee in enumerate(employees):
        if employee["id"] == id:
            employees.pop(index)
            break

def update_employee(id, new_employee):
    for index, employee in enumerate(employees):
        if employee["id"] == id:
            employees[index]["name"] = new_employee["name"]
            break
