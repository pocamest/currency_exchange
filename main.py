from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from typing import Any

FAKE_DB: dict[int, dict[str, Any]] = {
    0: {'name': "United States dollar", 'code': 'USD', "sign": "$"},
    1: {"name": "Euro", "code": "EUR", "sign": "€"},
}


def get_all_currencies() -> list[dict[str, Any]]:
    return [{'id': k} | v for k, v in FAKE_DB.items()]


def get_currency(code_currency: str) -> dict[str, Any]:
    for id, data in FAKE_DB.items():
        if data['code'] == code_currency:
            return {'id': id} | data
    return {}


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/currencies':
            payload = get_all_currencies()
            self._send_json_response(200, payload)

        elif self.path.startswith('/currencies'):
            try:
                code_currency = self.path.split('/')[2]
                payload = get_currency(code_currency)
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

                required_fields = ['id', 'name', 'code', 'sign']
                for field in required_fields:
                    if field not in data:
                        message = f'Отсутствует обязательное поле {field}'
                        self._send_json_error(400, message)
                        return

                new_currency = {
                    "id": data['id'],
                    "name": data['name'],
                    "code": data['code'],
                    "sign": data['sign']
                }

                FAKE_DB[data['id']] = new_currency

                self._send_json_response(201, new_currency)

            except json.JSONDecodeError:
                self._send_json_error(400, 'Неверный формат JSON')

            except Exception as e:
                self._send_json_error(500, f'Внутренняя ошибка сервера: {e}')

    def _send_json_response(
        self,
        status_code: int,
        payload: dict[str, Any] | list[dict[str, Any]]
    ):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(
            json.dumps(payload, ensure_ascii=False).encode('utf-8')
        )

    def _send_json_error(
        self,
        status_code: int,
        message: str
    ):
        error_payload = {'message': message}
        self._send_json_response(status_code, error_payload)


def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


if __name__ == '__main__':
    run_server()
