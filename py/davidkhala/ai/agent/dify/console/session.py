from base64 import b64encode

from requests.cookies import RequestsCookieJar

from davidkhala.ai.agent.dify.console import API


class ConsoleUser(API):
    def login(self, email, password,
              *,
              remember_me=True,
              language="en-US"
              ) -> RequestsCookieJar:
        url = f"{self.base_url}/login"

        r = self.request(url, "POST", json={
            'email': email,
            'password': b64encode(password.encode()).decode(),  # use base64 from dify 1.11
            'remember_me': remember_me,
            'language': language,
        })
        assert r == {"result": "success"}
        self.options['headers']['x-csrf-token'] = self.session.cookies.get("csrf_token")
        return self.session.cookies

    def set_tokens(self, *, csrf, access, refresh=None):
        """workaround for federated login"""
        self.session.cookies.set(name="__Host-csrf_token", value=csrf)
        self.session.cookies.set(name="__Host-access_token", value=access)
        if refresh:
            self.session.cookies.set(name="__Host-refresh_token", value=refresh)


        self.options['headers']['x-csrf-token'] = csrf

    @property
    def me(self) -> dict:
        url = f"{self.base_url}/account/profile"
        return self.request(url, "GET")

    @property
    def workspace(self) -> dict:
        url = f"{self.base_url}/features"
        return self.request(url, "GET")


class ConsoleDerived(API):
    def __init__(self, context: ConsoleUser):
        super().__init__()
        self.user = context
        self.base_url = context.base_url
        self.session.cookies = context.session.cookies
        self.options = context.options
