from http.server import HTTPServer

from api import CurrencyController, Router, create_handler
from config import DATABASE_PATH
from data import SQLiteConnectionFactory, SQLiteCurrencyDAO, SQLiteCurrencyRepository


def run_server(port: int = 8000) -> None:
    server_address = ('', port)
    currency_dao = SQLiteCurrencyDAO()
    connection_factory = SQLiteConnectionFactory(DATABASE_PATH)
    currency_repo = SQLiteCurrencyRepository(
        currency_dao=currency_dao,
        connection_factory=connection_factory,
    )
    currency_controller = CurrencyController(currency_repo)
    router = Router()
    router.add_route(
        method='GET',
        path='/currencies/',
        handler=currency_controller.get_all,
    )
    router.add_route(
        method='POST',
        path='/currencies/',
        handler=currency_controller.create_currency,
    )
    router.add_route(
        method='GET',
        path='/currencies/{code}',
        handler=currency_controller.get_by_code,
    )
    handler_class = create_handler(router)
    httpd = HTTPServer(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == '__main__':
    run_server()
