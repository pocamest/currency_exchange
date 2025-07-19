import json
from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler

from api.dtos import BaseDTO, ErrorDTO
from api.router import Router


def create_handler(router: Router) -> type[BaseHTTPRequestHandler]:
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

                parsed_data = parse_qs(post_data.decode('utf-8'))

                data = {key: value[0] for key, value in parsed_data.items()}

                handler = self._router.resolve(method=self.command, path=self.path)
                if not handler:
                    self._send_json_error(404, 'Ресурс не найден')
                    return
                status_code, payload = handler(data)
                self._send_json_response(status_code=status_code, payload=payload)
            except Exception as e:
                self._send_json_error(500, f'Внутренняя ошибка сервера: {e}')

        def _send_json_response(
            self, status_code: int, payload: BaseDTO | list[BaseDTO]
        ) -> None:
            self.send_response(status_code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            data = (
                [p.model_dump() for p in payload]
                if isinstance(payload, list)
                else payload.model_dump()
            )
            payload_json = json.dumps(data, ensure_ascii=False)
            self.wfile.write((payload_json).encode('utf-8'))

        def _send_json_error(self, status_code: int, message: str) -> None:
            self._send_json_response(status_code, ErrorDTO(message=message))

    return RequestHandler
