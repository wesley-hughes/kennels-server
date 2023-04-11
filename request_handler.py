import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_animals, get_single_animal, create_animal, delete_animal, update_animal, get_all_locations, get_single_location, create_location, delete_location, update_location, get_all_employees, get_single_employee, create_employee, delete_employee, update_employee, get_all_customers, get_single_customer, create_customer, delete_customer, update_customer

# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
method_mapper= {
    "animals" : {
        "all" : get_all_animals,
        "single" : get_single_animal
        },
    "locations" : {
        "all" : get_all_locations,
        "single" : get_single_location
        },
    "employees" : {
        "all" : get_all_employees,
        "single" : get_single_employee
        },
    "customers" : {
        "all" : get_all_customers,
        "single" : get_single_customer
        }
}
class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        '''docstring'''
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        # Try to get the item at index 2
        try:
            # Convert the string "1" to the integer 1
            # This is the new parseInt()
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id)  # This is a tuple

    def get_all_or_single(self, resource, id):
        if id is not None:
            response = method_mapper[resource]["single"](id)

            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = ''
        else:
            self._set_headers(200)
            response = method_mapper[resource]["all"]()

        return response
    def do_GET(self):
        response = None
        (resource, id) = self.parse_url(self.path)
        response = self.get_all_or_single(resource, id)
        self.wfile.write(json.dumps(response).encode())
    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        '''docstring'''
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)
        new_animal = None
        if resource == "animals":
            new_animal = create_animal(post_body)
            if "name" in post_body and "species" in post_body:
                self._set_headers(201)
                new_animal = new_animal(post_body)
            else:
                self._set_headers(400)
                new_animal = {"message": f'{"name is required" if "name" not in post_body else ""} {"species is required" if "species" not in post_body else ""}'}

        # Encode the new animal and send in response
        self.wfile.write(json.dumps(new_animal).encode())

        new_location = None
        if resource == "locations":
            new_location = create_location(post_body)
        self.wfile.write(json.dumps(new_location).encode())

        new_employee = None
        if resource == "employees":
            new_employee = create_employee(post_body)
        self.wfile.write(json.dumps(new_employee).encode())

        new_customer = None
        if resource == "customers":
            new_customer = create_customer(post_body)
        self.wfile.write(json.dumps(new_customer).encode())

    # A method that handles any PUT request.
    def do_PUT(self):
        '''docstring'''
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            update_animal(id, post_body)

        # Encode the new animal and send in response
        self.wfile.write("".encode())

        if resource == "locations":
            update_location(id, post_body)
        self.wfile.write("".encode())
        if resource == "customers":
            update_customer(id, post_body)
        self.wfile.write("".encode())
        if resource == "employees":
            update_employee(id, post_body)

        self.wfile.write("".encode())

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()
    def do_DELETE(self):
        '''docstring'''
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            self._set_headers(204)
            delete_animal(id)
        if resource == "locations":
            self._set_headers(204)
            delete_location(id)
        if resource == "employees":
            self._set_headers(204)
            delete_employee(id)
        if resource == "customers":
            self._set_headers(405)
            response = {"message": f'{"to delete customer, please contact admin"}'}
            self.wfile.write(json.dumps(response).encode())

        # Encode the new animal and send in response
        self.wfile.write("".encode())


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
