

class ProviderError(Exception):
    def __init__(self, message, code=None, api_response={}):
        self.message = message
        self.code = code
        self.api_response = api_response


class ServerError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


class ServiceUnavailable(ServerError):
    def __init__(self, message):
        self.message = message
