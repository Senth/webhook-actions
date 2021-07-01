from enum import Enum

from ...core.entities.action import Action
from .run_repo import RunRepo


class Output(Enum):
    success = 1
    fail = 2
    not_found = 3


class Run:
    def __init__(self, repo: RunRepo) -> None:
        self.repo = repo

    def execute(self, action: Action) -> Output:
        if not self.repo.exists(action):
            return Output.not_found

        success = self.repo.run(action)
        if not success:
            return Output.fail

        return Output.success
