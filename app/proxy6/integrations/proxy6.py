import httpx


class Proxy6Client:
    API_METHODS = (
        'getprice',
        'getcount',
        'getcountry',
        'getproxy',
        'settype',
        'setdescr',
        'buy',
        'prolong',
        'delete',
        'check'
    )

    def __init__(self, api_key):
        self.__api_key = api_key
        self.client = httpx.Client(base_url=f"https://proxy6.net/api/{api_key}", timeout=30)

    def __getattr__(self, item):
        if item in self.API_METHODS:
            def __method(**params):
                return self.api_call(item, params)
            return __method

    def api_call(self, method, params=None, hide_user_data=True):
        data = self.client.get(method, params=params).json()
        if hide_user_data:
            for key in ["user_id", "balance", "currency"]:
                if key in data:
                    del data[key]
        return data
