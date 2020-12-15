from dataclasses import dataclass


@dataclass
class Stop:
    id: str
    name: str
    direction: str
