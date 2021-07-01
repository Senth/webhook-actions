from enum import Enum

from ...config import config
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
        relative = action.path.split("/")
        script_path = config.webhook_dir.joinpath(*relative)

        if not self.repo.exists(script_path):
            return Output.not_found

        success = self.repo.run(script_path, action.data)
        if not success:
            return Output.fail

        return Output.success
