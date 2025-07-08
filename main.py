from http.server import HTTPServer, BaseHTTPRequestHandler
import json


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/currencies':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response_data = [
                {'id': 0, 'name': "United States dollar", 'code': 'USD', "sign": "$"},
                {"id": 0, "name": "Euro", "code": "EUR", "sign": "€"},
            ]
            self.wfile.write(json.dumps(response_data).encode('utf-8'))


# Потом попросить пояснить каждую строчку
def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == '__main__':
    run_server()
