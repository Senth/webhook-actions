import configparser
from pathlib import Path
from shutil import copy
from site import getuserbase
from typing import Any

from ..config import config
from .config_file_args import ConfigFileArgs


class ConfigFileParser:
    def __init__(self) -> None:
        self.filename = f".{config.app_name}.cfg"
        self.path = Path.home().joinpath(self.filename)

    def get_args(self) -> ConfigFileArgs:
        args = ConfigFileArgs()

        if not self.path.exists():
            return args

        config = configparser.ConfigParser()
        config.read(self.path)

        if "General" in config:
            args.port = ConfigFileParser._read_from_config(config["General"], "Port")

        return args

    @staticmethod
    def _read_from_config(config: configparser.SectionProxy, varname: str) -> Any:
        if varname in config:
            return config[varname]
        if varname.lower() in config:
            return config[varname]
        return None

    def create_if_not_exists(self) -> None:
        if self.path.exists():
            return

        # Copy file from config location to home
        original = Path(getuserbase()).joinpath("config", self.filename)

        if not original.exists():
            return

        copy(original, self.path)
