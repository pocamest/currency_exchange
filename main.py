from http.server import HTTPServer

from api import (
    CurrencyController,
    ExchangeRateController,
    Router,
    create_handler,
    register_routes,
)
from application import CurrencyService, ExchangeRateService
from config import CROSS_RATE_BASE_CURRENCY, DATABASE_PATH
from data import (
    SQLiteConnectionFactory,
    SQLiteCurrencyDAO,
    SQLiteCurrencyRepository,
    SQLiteExchangeRatesDAO,
    SQLiteExchangeRatesRepository,
)


def run_server(port: int = 8000) -> None:
    server_address = ('', port)
    connection_factory = SQLiteConnectionFactory(DATABASE_PATH)
    currency_dao = SQLiteCurrencyDAO()
    currency_repo = SQLiteCurrencyRepository(
        currency_dao=currency_dao, connection_factory=connection_factory
    )
    currency_service = CurrencyService(currency_repo)
    currency_controller = CurrencyController(currency_service)
    exchange_rate_dao = SQLiteExchangeRatesDAO()
    exchange_rate_repo = SQLiteExchangeRatesRepository(
        exchange_rate_dao=exchange_rate_dao, connection_factory=connection_factory
    )
    exchange_rate_service = ExchangeRateService(
        exchange_rate_repo=exchange_rate_repo,
        currency_repo=currency_repo,
        cross_rate_base_code=CROSS_RATE_BASE_CURRENCY,
    )
    exchange_rate_controller = ExchangeRateController(exchange_rate_service)
    router = Router()
    register_routes(
        router=router,
        currency_controller=currency_controller,
        exchange_rate_controller=exchange_rate_controller,
    )
    handler_class = create_handler(router)
    httpd = HTTPServer(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == '__main__':
    run_server()
