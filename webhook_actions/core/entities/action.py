from typing import Any, Dict


class Action:
    def __init__(self, name: str, trigger: str, data: Dict[str, Any]) -> None:
        self.name = name
        self.trigger = trigger
        self.data = data

    def __members(self):
        return [
            self.name,
            self.trigger,
        ]

    def test(self):
        return self.__members()

    def __eq__(self, other) -> bool:
        if type(other) is type(self):
            return self.__members() == other.__members()
        return False

    def __hash__(self) -> int:
        return hash(self.__members())
