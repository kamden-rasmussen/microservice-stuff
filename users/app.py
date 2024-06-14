from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests

class RouteHandler(BaseHTTPRequestHandler):
    routes = {
        'GET': {
            'users': lambda self: self.getUsers()
        },
        'POST': {
            'users': lambda self: self.saveUsers()
        }
    }

    users = [
        {
            'id': 1,
            'name': 'John Doe',
            'age': 25
        },
        {
            'id': 2,
            'name': 'Jane Doe',
            'age': 22
        }
    ]

        # phoneNumbers = {
        #         1: 1234567890,
        #         2: 2345678901,
        #         3: 3456789012,
        #     }


    @classmethod
    def register_route(cls, method, path, handler):
        cls.routes[method.upper()][path] = handler

    def do_GET(self):
        handler = self.find_handler('GET')
        if handler:
            handler(self)
        else:
            self.send_error(404, "Route not found")

    def do_POST(self):
        handler = self.find_handler('POST')
        if handler:
            handler(self)
        else:
            self.send_error(404, "Route not found")

    def find_handler(self, method):
        path = self.path.strip('/')
        return self.routes.get(method.upper(), {}).get(path)

    def getUsers(self):

        phoneNumbers = self.get_phonenumbers()
        for user in self.users:
            user_id = str(user.get('id'))
            if user_id in phoneNumbers:
                user['phonenumber'] = phoneNumbers[user_id]
            else:
                user['phonenumber'] = None

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(self.users).encode())

    def saveUsers(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        user = json.loads(post_data)
        self.users.append(user)
        self.save_phonenumber(user['id'], user['phonenumber'])
        self.send_header('Content-type', 'application/json')
        self.send_response(201)
        self.end_headers()
        self.wfile.write(json.dumps(user).encode())

    def get_phonenumbers(self) -> dict:

        url = 'http://localhost:3081/phonenumbers'

        response = requests.get(url)
        if response.status_code == 200:
            # convert the data into a dictionary
            data = json.loads(response.text)
            print('GET request to localhost:3081 succeeded:', data)
            return data
        else:
            print('GET request to localhost:3080 failed:', response.status_code)
            return {}

    def save_phonenumber(self, user_id, phonenumber) -> bool:
        url = 'http://localhost:3081/phonenumbers'
        print('POST request to localhost:3081:', user_id, phonenumber)
        data = {"id": user_id, "phonenumber": phonenumber}
        response = requests.post(url, data)
        if response.status_code == 201:
            print('POST request to localhost:3081 succeeded:', data)
            return True
        else:
            print('POST request to localhost:3081 failed:', response.status_code)
            return False


def run(server_class=HTTPServer, handler_class=RouteHandler, port=3080):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server listening on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
