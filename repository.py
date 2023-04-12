DATABASE = {
"animals" : [
    {
        "id": 1,
        "name": "Snickers",
        "species": "Dog",
        "locationId": 1,
        "customerId": 1,
        "status": "Admitted"
    },
    {
        "id": 2,
        "name": "Roman",
        "species": "Dog",
        "locationId": 1,
        "customerId": 1,
        "status": "Admitted"
    },
    {
        "id": 3,
        "name": "Blue",
        "species": "Cat",
        "locationId": 1,
        "customerId": 1,
        "status": "Admitted"
    }
],
"customers" : [
    {
        "id": 1,
        "name": "Ryan Tanay"
    }
],
"employees" : [
    {
        "id": 1,
        "name": "Jenna Solis"
    }
],
"locations" : [
    {
        "id": 1,
        "name": "Nashville North",
        "address": "8422 Johnson Pike"
    },
    {
        "id": 2,
        "name": "Nashville South",
        "address": "209 Emory Drive"
    }
]
}

def all(resources):
    """For GET requests to collection"""
    return DATABASE[resources]


def retrieve(resources, id):
    """For GET requests to a single resource"""
    requested_resource= None
    for resource in DATABASE[resources]:
        if resource["id"] == id:
            requested_resource = resource
            return requested_resource


def create(resources, resource):
    """For POST requests to a collection"""
    max_id = DATABASE[resources][-1]["id"]
    new_id = max_id + 1
    resource["id"] = new_id
    DATABASE[resources].append(resource)
    return resource


def update(resources, new_resource):
    """For PUT requests to a single resource"""
    for index, resource in enumerate(DATABASE[resources]):
        if resource["id"] == id:
            DATABASE[resources][index] = new_resource
            break


def delete(resources):
    """For DELETE requests to a single resource"""
    resources_index = -1
    for index, resource in enumerate(DATABASE[resources]):
        if resource["id"] == id:
            resources_index = index
    if resources_index >= 0:
        DATABASE[resources].pop(resources_index)
