from os import path, makedirs
from platform import system
from tempfile import gettempdir
from typing import Any, Union
import sys
import site
import importlib.util
import importlib.machinery
import argparse
import logging
import logging.handlers

_app_name = "webhook-actions"
_config_dir = path.join("config", _app_name)
_config_file = path.join(_config_dir, "config.py")
_example_file = path.join(_config_dir, "config.example.py")

# Search for config file in sys path
_sys_config = path.join(sys.prefix, _config_file)
_user_config_file = path.join(site.getuserbase(), _config_file)
_config_file = ""
if path.exists(_sys_config):
    _config_file = _sys_config
elif path.exists(_user_config_file):
    _config_file = _user_config_file
# User hasn't configured the program yet
else:
    _sys_config_example = path.join(sys.prefix, _example_file)
    _user_config_example = path.join(site.getuserbase(), _example_file)
    if not path.exists(_sys_config_example) and not path.exists(_user_config_example):
        print(
            f"Error: no configuration found. It should be here: '{_user_config_file}'"
        )
        print("run: locate " + _example_file)
        print("This should help you find the current config location.")
        print(
            f"Otherwise you can download the config.example.py from https://github.com/Senth/{_app_name}/tree/main/config and place it in the correct location"
        )
        sys.exit(1)

    print("This seems like it's the first time you run this program.")
    print(
        f"For this program to work properly you have to configure it by editing '{_user_config_file}'"
    )
    print(
        "In the same folder there's an example file 'config.example.py' you can copy to 'config.py'."
    )
    sys.exit(0)

# Import config
_loader = importlib.machinery.SourceFileLoader("config", _user_config_file)
_spec = importlib.util.spec_from_loader(_loader.name, _loader)
_user_config: Any = importlib.util.module_from_spec(_spec)
_loader.exec_module(_user_config)


def _print_missing(variable_name):
    print(f"Missing {variable_name} variable in config file: {_user_config_file}")
    print("Please add it to you config.py again to continue")
    sys.exit(1)


class Config:
    def __init__(self, user_config):
        self._user_config = user_config

        # Default values
        self.app_name: str = _app_name
        self.logger: logging.Logger
        self.debug: bool
        self.verbose: bool

        self._get_optional_variables()
        self._check_required_variables()
        self._parse_args()
        self._init_logger()

    def _parse_args(self):
        """Parse arguments from command line"""
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Prints out helpful messages.",
        )
        parser.add_argument(
            "--debug",
            action="store_true",
            help="Turn on debug messages. This automatically turns on --verbose as well.",
        )

        _args = parser.parse_args()
        self._add_args_settings(_args)

    def _add_args_settings(self, args):
        """Set additional configuration from script arguments

        Args:
            args (list): All the parsed arguments
        """
        self.verbose = args.verbose
        self.debug = args.debug

        if args.debug:
            self.verbose = True

    def _get_optional_variables(self):
        """Get optional values from the config file"""
        # try:
        #     self.log_dir = _user_config.LOG_DIR
        # except AttributeError:
        #     pass

    def _check_required_variables(self):
        """Check that all required variables are set in the user config file"""
        # try:
        #     self.port = _user_config.PORT
        # except AttributeError:
        #     _print_missing("PORT")

    def _init_logger(self):
        os = system()
        if os == "Windows":
            log_dir = path.join(gettempdir(), _app_name)
            makedirs(log_dir, exist_ok=True)
        else:
            # TODO create dir, or log in a home directory
            log_dir = f"/var/log/{_app_name}/"
        log_location = path.join(log_dir, f"{_app_name}.log")

        if self.debug:
            log_level = logging.DEBUG
        elif self.verbose:
            log_level = logging.INFO
        else:
            log_level = logging.INFO

        # Set logging rotation
        timed_rotating_handler = logging.handlers.TimedRotatingFileHandler(
            log_location, when="midnight"
        )
        timed_rotating_handler.setLevel(log_level)
        timed_rotating_handler.setFormatter(
            logging.Formatter(
                "\033[1m%(asctime)s:%(levelname)s:\033[0m %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )

        # Stream output
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(log_level)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.logger.addHandler(timed_rotating_handler)
        self.logger.addHandler(stream_handler)


global config
config = Config(_user_config)
