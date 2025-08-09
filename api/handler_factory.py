import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

from api.dtos import BaseDTO, ErrorDTO
from api.router import Router


def create_handler(router: Router) -> type[BaseHTTPRequestHandler]:
    class RequestHandler(BaseHTTPRequestHandler):
        _router = router

        def do_GET(self) -> None:
            self._handle_request_without_body()

        def do_POST(self) -> None:
            self._handle_request_with_body()

        def do_PATCH(self) -> None:
            self._handle_request_with_body()

        def _send_json_response(
            self, status_code: int, payload: BaseDTO | list[BaseDTO]
        ) -> None:
            self.send_response(status_code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            data = (
                [p.model_dump(by_alias=True) for p in payload]
                if isinstance(payload, list)
                else payload.model_dump(by_alias=True)
            )
            payload_json = json.dumps(data, ensure_ascii=False)
            self.wfile.write((payload_json).encode('utf-8'))

        def _send_json_error(self, status_code: int, message: str) -> None:
            self._send_json_response(status_code, ErrorDTO(message=message))

        def _handle_request_without_body(self) -> None:
            try:
                parsed_path = urlparse(self.path)
                path_only = parsed_path.path
                handler, path_params = self._router.resolve(
                    method=self.command, path=path_only
                )
                if not handler or path_params is None:
                    self._send_json_error(404, 'Ресурс не найден')
                    return

                if parsed_path.query:
                    parsed_query_params = parse_qs(parsed_path.query)
                    query_params = {k: v[0] for k, v in parsed_query_params.items()}
                else:
                    query_params = {}

                kwargs = {**path_params, **query_params}

                status_code, payload = handler(**kwargs)
                self._send_json_response(status_code=status_code, payload=payload)
            except Exception as e:
                self._send_json_error(500, f'Внутренняя ошибка сервера: {e}')

        def _handle_request_with_body(self) -> None:
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)

                parsed_data = parse_qs(post_data.decode('utf-8'))

                body = {key: value[0] for key, value in parsed_data.items()}

                parsed_path = urlparse(self.path)
                path_only = parsed_path.path

                handler, path_params = self._router.resolve(
                    method=self.command, path=path_only
                )
                if not handler or path_params is None:
                    self._send_json_error(404, 'Ресурс не найден')
                    return

                if parsed_path.query:
                    parsed_query_params = parse_qs(parsed_path.query)
                    query_params = {k: v[0] for k, v in parsed_query_params.items()}
                else:
                    query_params = {}

                kwargs = {**path_params, **query_params}

                status_code, payload = handler(body=body, **kwargs)
                self._send_json_response(status_code=status_code, payload=payload)
            except Exception as e:
                self._send_json_error(500, f'Внутренняя ошибка сервера: {e}')

    return RequestHandler
