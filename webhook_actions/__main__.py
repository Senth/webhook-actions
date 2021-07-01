from .adapters.app_impl import AppImpl
from .config import config
from .gateways.flask_gateway import FlaskGateway
from .utils.arg_parser import get_args
from .utils.config_file_parser import ConfigFileParser


def main():
    config.set_from_config_file(ConfigFileParser().get_args())
    config.set_args_settings(get_args())

    flask_gateway = FlaskGateway()
    flask_gateway.app = AppImpl()
    flask_gateway.listen()


if __name__ == "__main__":
    main()
