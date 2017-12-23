from gpayments import util


class GpaymentsResponse:

    def __init__(self, body, code, headers):
        self.body = body
        self.code = code
        self.headers = headers
        self.data = util.json.loads(body)

    @property
    def request_id(self):
        try:
            return self.headers['request-id']
        except KeyError:
            return None
