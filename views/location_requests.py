import sqlite3
import json
from models import Location
LOCATIONS = [
    {
        "id": 1,
        "name": "Nashville North",
        "address": "8422 Johnson Pike"
    },
    {
        "id": 2,
        "name": "Nashville South",
        "address": "209 Emory Drive"
    },
    {
        "name": "Nashville East",
        "address": " 1901 Gallatin Pike",
        "id": 3
    }
]


def get_all_locations():
    '''fetches all locations from the database'''
    # Establishing a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Configuring the connection to return rows as dictionaries
        conn.row_factory = sqlite3.Row

        # Creating a database cursor
        db_cursor = conn.cursor()

        # Executing an SQL query to select all locations from the database
        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address
        FROM location l
        """)

        # Fetching all the data returned by the SQL query
        dataset = db_cursor.fetchall()

        # Creating an empty list to store the Location objects
        locations = []

        # Looping through the fetched data and creating Location objects
        for row in dataset:

            # Creating a Location object for each row of data
            location = Location(row['id'], row['name'], row['address'])

            # Appending the dictionary representation of the Location object to the list
            locations.append(location.__dict__)

    # Returning the list of Location objects as dictionaries
    return locations


def get_single_location(id):
    '''fetches a single location from the database based on the ID provided'''
    # Establishing a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Configuring the connection to return rows as dictionaries
        conn.row_factory = sqlite3.Row

        # Creating a database cursor
        db_cursor = conn.cursor()

        # Executing an SQL query to select a single location from the database
        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address
        FROM location l
        WHERE l.id =?
        """, (id, ))

        # Fetching the single row of data returned by the SQL query
        data = db_cursor.fetchone()

        # Creating a Location object for the fetched data
        location = Location(data['id'], data['name'], data['address'])

        # Returning the dictionary representation of the Location object
        return location.__dict__


def create_location(location):
    '''creates new location'''
    max_id = LOCATIONS[-1]["id"]
    new_id = max_id + 1
    location["id"] = new_id
    LOCATIONS.append(location)
    return location


def delete_location(id):
    '''deletes location by id'''
    location_index = -1

    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            location_index = index

    if location_index >= 0:
        LOCATIONS.pop(location_index)


def update_location(id, new_location):
    '''updates location by id'''
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            LOCATIONS[index] = new_location
            break
