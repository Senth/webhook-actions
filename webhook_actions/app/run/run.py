from enum import Enum

from ...core.entities.action import Action
from .run_repo import RunRepo


class RunOutput(Enum):
    success = 1
    fail = 2
    not_found = 3


class Run:
    def __init__(self, repo: RunRepo) -> None:
        self.repo = repo

    def execute(self, action: Action) -> RunOutput:
        if not self.repo.exists(action):
            return RunOutput.not_found

        success = self.repo.run(action)
        if not success:
            return RunOutput.fail

        return RunOutput.success
