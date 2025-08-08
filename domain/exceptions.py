class AppError(Exception):
    pass


class NotFoundError(AppError):
    pass


class ConflictError(AppError):
    pass


class SystemError(AppError):
    pass


class ConfigurationError(AppError):
    pass
