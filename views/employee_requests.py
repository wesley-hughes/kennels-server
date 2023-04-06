EMPLOYEES = [
    {
        "id": 1,
        "name": "Jenna Solis"
    }
]

def get_all_employees():
    '''this gets all employees'''
    return EMPLOYEES
def get_single_employee(id):
    '''this gets single employee by id'''
    requested_employee= None
    for employee in EMPLOYEES:
        if employee["id"] == id:
            requested_employee = employee
        return requested_employee
def create_employee(employee):
    '''creates new employee'''
    max_id = EMPLOYEES[-1]["id"]
    new_id = max_id + 1
    employee["id"] = new_id
    EMPLOYEES.append(employee)
    return employee
def delete_employee(id):
    '''docstring'''
    employee_index = -1
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            employee_index = index
    if employee_index >= 0:
        EMPLOYEES.pop(employee_index)
def update_employee(id, new_employee):
    '''docstring'''
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            # Found the    employee. Update the value.
            EMPLOYEES[index] = new_employee
            break