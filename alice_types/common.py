from typing import List


class AvailableMixin:
    def available(self) -> List[str]:
        available = []
        for name, value in self.__dict__.items():
            if value is not None:
                available.append(name)
        
        return available
