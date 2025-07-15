from http.server import HTTPServer

from config import DATABASE_PATH
from data import SQLiteConnectionFactory, SQLiteCurrencyDAO, SQLiteCurrencyRepository
from request_handler import create_handler


def run_server(port: int =8000) -> None:
    server_address = ('', port)
    currency_dao = SQLiteCurrencyDAO()
    connection_factory = SQLiteConnectionFactory(DATABASE_PATH)
    currency_repo = SQLiteCurrencyRepository(
        currency_dao=currency_dao,
        connection_factory=connection_factory,
    )
    handler_class = create_handler(currency_repo)
    httpd = HTTPServer(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == '__main__':
    run_server()
