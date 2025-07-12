import json
from http.server import BaseHTTPRequestHandler
from typing import Any

from database.repositories import AbstractCurrencyRepository


def create_handler(
    currency_rep: AbstractCurrencyRepository,
) -> type[BaseHTTPRequestHandler]:
    class RequestHandler(BaseHTTPRequestHandler):
        _currency_rep = currency_rep

        def do_GET(self):
            if self.path == '/currencies':
                payload = self._currency_rep.find_all()
                self._send_json_response(200, payload)

            elif self.path.startswith('/currencies'):
                try:
                    code_currency = self.path.split('/')[2]
                    payload = self._currency_rep.find_by_code(code_currency)
                    if not payload:
                        self._send_json_error(404, 'Ресурс не найден')
                    self._send_json_response(200, payload)
                except IndexError:
                    self._send_json_error(404, 'Ресурс не найден')

            else:
                self._send_json_error(404, 'Ресурс не найден')

        def do_POST(self):
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

                    created_currency = self._currency_rep.create(
                        data['code'], data['name'], data['sign']
                    )

                    self._send_json_response(201, created_currency)

                except json.JSONDecodeError:
                    self._send_json_error(400, 'Неверный формат JSON')

                except Exception as e:
                    self._send_json_error(500, f'Внутренняя ошибка сервера: {e}')

        def _send_json_response(
            self, status_code: int, payload: dict[str, Any] | list[dict[str, Any]]
        ):
            self.send_response(status_code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(payload, ensure_ascii=False).encode('utf-8'))

        def _send_json_error(self, status_code: int, message: str):
            error_payload = {'message': message}
            self._send_json_response(status_code, error_payload)

    return RequestHandler
