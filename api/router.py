from collections.abc import Callable
from typing import Any


class Router:
    def __init__(self) -> None:
        self.routes: dict[tuple[str, str], Callable[..., Any]] = {}

    def add_route(self, method: str, path: str, handler: Callable[..., Any]) -> None:
        self.routes[(method, path)] = handler

    def resolve(self, method: str, path: str) -> Callable[..., Any] | None:
        return self.routes.get((method, path))
