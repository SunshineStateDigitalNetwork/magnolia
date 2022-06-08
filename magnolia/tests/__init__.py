import configparser
import sys
from pathlib import Path

from .exceptions_test import *
from .harvest_test import *
from .maps_test import *
from .organiztions_test import *
from .scenarios_test import *
from .source_resource_test import *
from .transform_test import *

if __name__ == 'magnolia.tests':
    # Locating configs
    if os.getenv('MAGNOLIA_CONFIG'):
        CONFIG_PATH = Path(os.getenv('MAGNOLIA_CONFIG'))
    elif os.path.exists(os.path.join(Path.home(), '.local/share/magnolia/magnolia.cfg')):
        CONFIG_PATH = os.path.join(Path.home(), '.local/share/magnolia')
    elif os.path.exists(os.path.join(Path(__file__).parents[0], 'magnolia.cfg')):
        CONFIG_PATH = Path(__file__).parents[0]
    else:
        CONFIG_PATH = None

    try:
        magnolia_config = configparser.ConfigParser()
        magnolia_config.read(os.path.join(CONFIG_PATH, 'magnolia.cfg'))
        for profile in magnolia_config.keys():
            custom_map_test_path = magnolia_config[profile]['CustomMapPath']
            try:
                sys.path.append(custom_map_test_path)
                from custom_map_tests import *
            except (ModuleNotFoundError, NameError):
                pass
    except TypeError:
        pass
