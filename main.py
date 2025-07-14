from http.server import HTTPServer

from config import DATABASE_PATH
from data.connection import SQLiteConnection
from data.daos import SQLiteCurrenctDAO
from data.repositories import SQLiteCurrencyRepository
from request_handler import create_handler


def run_server(port=8000):
    server_address = ('', port)
    currency_dao = SQLiteCurrenctDAO()
    database_connection = SQLiteConnection(DATABASE_PATH)
    currency_repo = SQLiteCurrencyRepository(currency_dao, database_connection)
    handler_class = create_handler(currency_repo)
    httpd = HTTPServer(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == '__main__':
    run_server()
