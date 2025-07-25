from http.server import HTTPServer

from api import CurrencyController, Router, create_handler, register_routes
from config import DATABASE_PATH
from data import SQLiteConnectionFactory, SQLiteCurrencyDAO, SQLiteCurrencyRepository
from domain import CurrencyService


def run_server(port: int = 8000) -> None:
    server_address = ('', port)
    currency_dao = SQLiteCurrencyDAO()
    connection_factory = SQLiteConnectionFactory(DATABASE_PATH)
    currency_repo = SQLiteCurrencyRepository(
        currency_dao=currency_dao,
        connection_factory=connection_factory,
    )
    currency_service = CurrencyService(currency_repo)
    currency_controller = CurrencyController(currency_service)
    router = Router()
    register_routes(router=router, currency_controller=currency_controller)
    handler_class = create_handler(router)
    httpd = HTTPServer(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == '__main__':
    run_server()
