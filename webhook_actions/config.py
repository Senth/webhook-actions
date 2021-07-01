from pathlib import Path

from .utils.config_file_args import ConfigFileArgs

_app_name = "webhook-actions"


class Config:
    def __init__(self):
        # Default values
        self.app_name: str = _app_name
        self.webhook_dir = Path.home().joinpath(self.app_name)
        self.debug: bool = False
        self.verbose: bool = False
        self.port: int = 5000

    def add_args_settings(self, args):
        """Set additional configuration from script arguments"""
        self.verbose = args.verbose
        self.debug = args.debug

        if args.debug:
            self.verbose = True

    def set_from_config_file(self, args: ConfigFileArgs) -> None:
        if args.port:
            self.port = args.port


config = Config()
