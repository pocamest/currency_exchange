from api.controllers import CurrencyController
from api.router import Router


def register_routes(router: Router, currency_controller: CurrencyController) -> None:
    router.add_route(
        method='GET',
        path='/currencies/',
        handler=currency_controller.get_all_currencies,
    )
    router.add_route(
        method='POST',
        path='/currencies/',
        handler=currency_controller.create_currency,
    )
    router.add_route(
        method='GET',
        path='/currencies/{code}',
        handler=currency_controller.get_currency_by_code,
    )
