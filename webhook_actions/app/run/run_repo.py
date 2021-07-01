from pathlib import Path


class RunRepo:
    def run(self, script: Path, arg: str) -> bool:
        raise NotImplementedError()

    def exists(self, file: Path) -> bool:
        raise NotImplementedError()
