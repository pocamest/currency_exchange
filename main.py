from http.server import HTTPServer

from config import DATABASE_PATH
from database.repositories import SQLiteCurrencyRepository
from request_handler import create_handler


def run_server(port=8000):
    server_address = ('', port)
    currency_repo = SQLiteCurrencyRepository(DATABASE_PATH)
    Handler = create_handler(currency_repo)
    httpd = HTTPServer(server_address, Handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == '__main__':
    run_server()
