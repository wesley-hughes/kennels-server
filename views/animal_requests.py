import sqlite3
from models import Animal, Location
from .customer_requests import get_single_customer
from .location_requests import get_single_location

def get_all_animals(query_params):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        sort_by = ""
        where_clause = ""
        if len(query_params) != 0:
            param = query_params[0]
            [qs_key, qs_value] = param.split("=")

            if qs_key == "_sortBy":
                if qs_value == 'location':
                    sort_by = " ORDER BY location_id"
                if qs_value == 'customer':
                    sort_by = " ORDER BY customer_id "
                if qs_value == 'status':
                    sort_by = "ORDER BY status ASC"
                if qs_value == "name":
                    sort_by = "ORDER BY a.name ASC"
            if qs_key == "locationId":
                where_clause = f"WHERE a.location_id = {qs_value}"
            if qs_key == "status":
                where_clause = f"WHERE a.status = '{qs_value}'"
        sql_to_execute = f"""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            l.name location_name,
            l.address location_address
        FROM Animal a
        JOIN Location l ON l.id = a.location_id
        {sort_by}
        {where_clause}"""
        db_cursor.execute(sql_to_execute)
        animals = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            animal = Animal(row['id'], row['name'], row['breed'], row['status'], row['location_id'], row['customer_id'])
            
            animals.append(animal.__dict__)
        return animals
# Function with a single parameter
def get_single_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            a.id,
            a.name name,
            a.status,
            a.breed,
            a.customer_id,
            a.location_id,
            c.name,
            l.name
        FROM Animal a
        LEFT JOIN Customer c ON c.id = a.customer_id
        LEFT JOIN Location l ON l.id = a.location_id
        WHERE a.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

       
        animal = Animal(data['id'],data['name'], data['status'], data['breed'], data['customer_id'], data['location_id'])
        animal.customer = get_single_customer(data['customer_id'])
        animal.location = get_single_location(data['location_id'])
        return animal.__dict__
def get_animals_by_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            a.id,
            a.name name,
            a.status,
            a.breed,
            a.customer_id,
            a.location_id,
            c.name,
            l.name
        FROM Animal a
        LEFT JOIN Customer c ON c.id = a.customer_id
        LEFT JOIN Location l ON l.id = a.location_id
        WHERE a.id = ?
        """, (id, ))

        data = db_cursor.fetchone()

       
        animal = Animal(data['id'],data['name'], data['status'], data['breed'], data['customer_id'], data['location_id'])
        animal.customer = get_single_customer(data['customer_id'])
        animal.location = get_single_location(data['location_id'])
        return animal.__dict__
def get_animals_by_term(term):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name name,
            a.status,
            a.breed,
            a.customer_id,
            a.location_id,
            c.name,
            l.name
        FROM Animal a
        LEFT JOIN Customer c ON c.id = a.customer_id
        LEFT JOIN Location l ON l.id = a.location_id
        WHERE a.name LIKE ?
        """, ( f"%{term}%", ))

        animals = []
        dataset = db_cursor.fetchall()
        for row in dataset:

            animal = Animal(row['id'], row['name'], row['breed'], row['status'], row['location_id'], row['customer_id'])
            
            animals.append(animal.__dict__)
        return animals

def create_animal(new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Animal
            ( name, status, breed, customer_id, location_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_animal['name'], new_animal['status'],
              new_animal['breed'], new_animal['customer_id'], new_animal['location_id'] ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_animal['id'] = id
    return new_animal

def delete_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        DELETE FROM Animal
        WHERE id = ?
        """, (id, ))
def update_animal(id, new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute("""
        UPDATE Animal
             SET
                name = ?,
                status = ?,
                breed = ?,
                customer_id,
                location_id   
        WHERE id = ?
        """, (new_animal['name'], new_animal['status'], new_animal['breed'], new_animal['customer_id'],new_animal['location_id'], id, ))
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
            # Forces 404 response by main module
        return False
    else:
            # Forces 204 response by main module
        return True