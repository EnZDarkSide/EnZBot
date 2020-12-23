from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Stop:
    name: str
    # [(123, 'direction name 1'), (124, 'direction name 2')]
    directions: List[Tuple[int, str]]
