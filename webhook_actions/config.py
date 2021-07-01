from pathlib import Path

_app_name = "webhook-actions"


class Config:
    def __init__(self):

        # Default values
        self.app_name: str = _app_name
        self.webhook_dir = Path("~/webhook-actions").expanduser()
        self.debug: bool = False
        self.verbose: bool = False

    def add_args_settings(self, args):
        """Set additional configuration from script arguments"""
        self.verbose = args.verbose
        self.debug = args.debug

        if args.debug:
            self.verbose = True


config = Config()
