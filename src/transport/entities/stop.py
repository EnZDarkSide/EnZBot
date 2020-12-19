from dataclasses import dataclass
from typing import Union


@dataclass
class Stop:
    id: int
    name: str
    direction: Union[str, None]

    @property
    def title(self) -> str:
        return f'{self.name} ' + (f'({self.direction})' if self.direction else '')
