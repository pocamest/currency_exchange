import json
from http.server import BaseHTTPRequestHandler

from data import AbstractCurrencyRepository
from domain import Currency


def create_handler(
    currency_repo: AbstractCurrencyRepository,
) -> type[BaseHTTPRequestHandler]:
    class RequestHandler(BaseHTTPRequestHandler):
        _currency_repo = currency_repo

        def do_GET(self) -> None:
            if self.path == '/currencies':
                payload: list[Currency] = self._currency_repo.find_all()
                self._send_json_response(200, payload)

            elif self.path.startswith('/currencies'):
                try:
                    code_currency = self.path.split('/')[2]
                    payload: Currency | None = self._currency_repo.find_by_code(
                        code_currency
                    )
                    if not payload:
                        self._send_json_error(404, 'Ресурс не найден')
                        return
                    self._send_json_response(200, payload)
                except IndexError:
                    self._send_json_error(404, 'Ресурс не найден')

            else:
                self._send_json_error(404, 'Ресурс не найден')

        def do_POST(self) -> None:
            if self.path == '/currencies':
                try:
                    content_length = int(self.headers.get('Content-Length', 0))
                    post_data = self.rfile.read(content_length)

                    data = json.loads(post_data.decode('utf-8'))

                    required_fields = ['name', 'code', 'sign']
                    for field in required_fields:
                        if field not in data:
                            message = f'Отсутствует обязательное поле {field}'
                            self._send_json_error(400, message)
                            return

                    created_currency = self._currency_repo.create(
                        data['code'], data['name'], data['sign']
                    )

                    self._send_json_response(201, created_currency)

                except json.JSONDecodeError:
                    self._send_json_error(400, 'Неверный формат JSON')

                except Exception as e:
                    self._send_json_error(500, f'Внутренняя ошибка сервера: {e}')

        def _send_json_response(
            self, status_code: int, payload: Currency | list[Currency]
        ) -> None:
            self.send_response(status_code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            if isinstance(payload, list):
                payload_json = (
                    f'[{",".join(x.model_dump_json(by_alias=True) for x in payload)}]'
                )
            else:
                payload_json = payload.model_dump_json(by_alias=True)
            self.wfile.write((payload_json).encode('utf-8'))

        def _send_json_error(self, status_code: int, message: str) -> None:
            error_payload = {'message': message}
            self.send_response(status_code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(
                json.dumps(error_payload, ensure_ascii=False).encode('utf-8')
            )

    return RequestHandler
