from dataclasses import dataclass, field


@dataclass
class User:
    username: str
    password: str = field(repr=False)


