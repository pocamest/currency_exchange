import json
from http.server import BaseHTTPRequestHandler

from api.router import Router
from domain import Currency


def create_handler(
    router: Router
) -> type[BaseHTTPRequestHandler]:
    class RequestHandler(BaseHTTPRequestHandler):
        _router = router

        def do_GET(self) -> None:
            handler = self._router.resolve(method=self.command, path=self.path)
            if not handler:
                self._send_json_error(404, 'Ресурс не найден')
                return
            status_code, payload = handler()
            self._send_json_response(status_code=status_code, payload=payload)


        def do_POST(self) -> None:
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)

                data = json.loads(post_data.decode('utf-8'))
                handler = self._router.resolve(method=self.command, path=self.path)
                if not handler:
                    self._send_json_error(404, 'Ресурс не найден')
                    return
                status_code, payload = handler(code=data['code'], full_name=data['name'], sign=data['sign'])
                self._send_json_response(status_code=status_code, payload=payload)
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
