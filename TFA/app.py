from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class RouteHandler(BaseHTTPRequestHandler):
    routes = {
        'GET': {
            'phonenumbers': lambda self: self.getPhoneNumbers()
        },
        'POST': {
            'phonenumbers': lambda self: self.savePhoneNumbers()
        }
    }

    phoneNumbers = {
            1: 1234567890,
            2: 2345678901,
            3: 3456789012,
        }


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

    def getPhoneNumbers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(self.phoneNumbers).encode())
        return

    def savePhoneNumbers(self):
        print('Saving phone numbers')
        content_length = int(self.headers['Content-Length'])
        print(content_length)
        post_data = self.rfile.read(content_length)
        print(post_data)
        phone = json.loads(post_data)
        print(phone)
#       if there is no ID or phonenumber in the post request, return 400
        if 'id' not in phone or 'phonenumber' not in phone:
            self.send_response(400)
            print('No ID or phonenumber in post request')
            return
        print("success")
        self.phoneNumbers.update({phone['id']: phone['phonenumber']})
        print(self.phoneNumbers)
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        content_length = len(json.dumps(self.phoneNumbers))
        self.send_header('Content-Length', str(content_length))
        self.end_headers()
        self.wfile.write(json.dumps(self.phoneNumbers).encode())
        return


def run(server_class=HTTPServer, handler_class=RouteHandler, port=3081):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server listening on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
