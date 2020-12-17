from dataclasses import dataclass


@dataclass
class Stop:
    id: int
    name: str
    direction: str
