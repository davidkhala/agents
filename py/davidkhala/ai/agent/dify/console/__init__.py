from davidkhala.utils.http_request import Request


class API(Request):

    def __init__(self, base_url='http://localhost'):
        """
        :param base_url: "{protocol}://{host}". For Dify cloud, it is 'https://cloud.dify.ai'
        """
        super().__init__()
        self.base_url = f"{base_url}/console/api"
        self.open()

