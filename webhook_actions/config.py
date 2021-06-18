from .utils.arg_parser import get_args

_app_name = "webhook-actions"


class Config:
    def __init__(self):

        # Default values
        self.app_name: str = _app_name
        self.debug: bool
        self.verbose: bool

        self._add_args_settings()

    def _add_args_settings(self):
        """Set additional configuration from script arguments"""
        args = get_args()
        self.verbose = args.verbose
        self.debug = args.debug

        if args.debug:
            self.verbose = True


config = Config()
