import httpx


class Yoomoney:
    base_url = ''

    def __init__(self, access_token: str):
        self.__access_token = access_token
        self.client = httpx.Client(base_url=self.base_url, headers={
            'Authorization': self.__access_token
        })

    def request(self, method, path, params=None, data=None):
        response = self.client.request(method, path, data=data, params=params)
        return response.json()

    def request_payment(self, wallet, amount):
        data = {
            'pattern_id': 'p2p',
            'to': wallet,
            'amount': amount
        }
        return self.request('POST', 'request-payment', data=data)

    def process_payment(self, request_id):
        data = {
            'request_id': request_id
        }
        return self.request('POST', 'process-payment', data=data)
