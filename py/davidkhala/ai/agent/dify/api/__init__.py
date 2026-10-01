from typing import Iterable, Callable, Any

from davidkhala.utils.http_request import Request


class API(Request):
    """public API"""
    def __init__(self, api_key: str, base_url="https://api.dify.ai/v1"):
        super().__init__({'bearer': api_key})
        self.base_url = base_url
        self.api_key = api_key


class Iterator(Iterable):
    def __iter__(self):
        return self

    def __init__(self, get_fn: Callable[[int, int, str], Any], *, size=20, keyword=None):
        self.last_response = None
        self.keyword = keyword
        self.size = size
        self.fn = get_fn

    def __next__(self):
        if self.last_response and not self.last_response['has_more']:
            raise StopIteration
        page = 1 if not self.last_response else self.last_response['page'] + 1
        self.last_response = self.fn(page, self.size, self.keyword)
        return self.last_response['data']
