from davidkhala.utils.dantic.models import ID


class User(ID):
    name: str
    email: str
