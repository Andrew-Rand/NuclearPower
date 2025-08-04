from abc import ABC, abstractmethod


class BaseUnit(ABC):

    @property
    @abstractmethod
    def conditions(self) -> dict[str, int | float]:
        pass

    @abstractmethod
    async def update_conditions(self):
        pass