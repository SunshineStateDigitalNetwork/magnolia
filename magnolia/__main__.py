"""
Command-line interface when the module is called with `python3 -m magnolia`.

Most actions can be explored with the `--help` flag.

The two main activities are:
    * `harvest` (defined in `magnolia.cli.harvest`)
    * `transform` (defined in `magnolia.cli.transform`)

Other command options relate to setting and querying the program environment and running the module self-test.

The path to the magnolia configuration files must either be defined with the `MAGNOLIA_CONFIG` environment variable or exist in one of two default locations:
    * $HOME/.local/share/magnolia
    * the magnolia module directory

"""

import configparser
import logging
import os
import sys
from pathlib import Path

import magnolia
from magnolia import cli

logger = logging.getLogger('magnolia.app')
logger.addHandler(logging.NullHandler())

if __name__ == '__main__':

    # Locating configs
    if os.getenv('MAGNOLIA_CONFIG'):
        CONFIG_PATH = Path(os.getenv('MAGNOLIA_CONFIG'))
    elif os.path.exists(os.path.join(Path.home(), '.local/share/magnolia/magnolia.cfg')):
        CONFIG_PATH = os.path.join(Path.home(), '.local/share/magnolia')
    elif os.path.exists(os.path.join(Path(__file__).parents[0], 'magnolia.cfg')):
        CONFIG_PATH = Path(__file__).parents[0]
    else:
        print("Cannot locate magnolia configs.")
        build_configs = str(input('\nBuild empty configs? (y/n) >>> ')).lower()
        if build_configs == 'y':
            os.makedirs(os.path.join(Path.home(), '.local/share/magnolia/'), exist_ok=True)
            with open(os.path.join(Path.home(), '.local/share/magnolia/magnolia.cfg'), 'w') as magnolia_cfg:
                magnolia_cfg.write(cli.empty_magnolia_cfg)
            with open(os.path.join(Path.home(), '.local/share/magnolia/magnolia_harvests.cfg'), 'w') as harvest_cfg:
                harvest_cfg.write(cli.empty_harvest_cfg)
            with open(os.path.join(Path.home(), '.local/share/magnolia/magnolia_scenarios.cfg'), 'w') as scenario_cfg:
                scenario_cfg.write(cli.empty_scenario_cfg)
            print(f"\nEmpty config files are located at {os.path.join(Path.home(), '.local/share/magnolia/')}")
            sys.exit(0)
        elif build_configs == 'n':
            print('\nOk. Please see magnolia configuration documentation: www.example.org')
            sys.exit(0)
        else:
            print(
                "\nI'm sorry, I didn't understand that.\nPlease see magnolia configuration documentation: www.example.org")
            sys.exit(1)

    #############################
    # Application configuration #
    #############################

    # magnolia application config
    magnolia_config = configparser.ConfigParser()
    magnolia_config.read(os.path.join(CONFIG_PATH, 'magnolia.cfg'))

    # cli application arguments
    args = cli.argument_parser().parse_args()

    #######################
    # Application actions #
    #######################

    # Verbosity
    verbosity = 1
    if args.verbose:
        verbosity = 2

    # Profile selection
    profile = 'DEFAULT'
    if args.profile:
        profile = args.profile
        try:
            magnolia_config[profile]
        except KeyError:
            logger.error(f"Profile: {profile} is not listed in {os.path.join(CONFIG_PATH, 'magnolia.cfg')}")
            raise magnolia.exceptions.MagnoliaPofileError(profile, os.path.join(CONFIG_PATH, 'magnolia.cfg'))

    # Set up logging

    # TODO: configing arbitrary handlers and filters

    # Log path
    try:
        LOG_PATH = os.path.abspath(magnolia_config[profile]['LogPath'])
    except KeyError:
        LOG_PATH = Path.home()
    # Log level
    try:
        LOG_LEVEL = magnolia_config[profile]['LogLevel']
    except KeyError:
        LOG_LEVEL = 'warning'
    app_logger = logging.getLogger()

    # default handler
    log_fh = logging.FileHandler(os.path.join(LOG_PATH, 'magnolia.log'))
    formatter = logging.Formatter('%(name)s: %(asctime)s: %(levelname)s: %(message)s', datefmt='%Y-%m-%d, %I:%M')
    log_fh.setFormatter(formatter)
    log_fh.setLevel(logging.DEBUG)

    # TSV handler
    tsv_fh = logging.FileHandler(os.path.join(LOG_PATH, 'magnolia_errors.tsv'))
    tsv_formatter = logging.Formatter('%(name)s\t%(asctime)s\t%(levelname)s\t%(message)s', datefmt='%Y-%m-%d, %I:%M')
    tsv_fh.setFormatter(tsv_formatter)
    tsv_fh.setLevel(logging.WARNING)

    app_logger.setLevel(LOG_LEVEL.upper())
    app_logger.addHandler(log_fh)
    app_logger.addHandler(tsv_fh)

    logger.debug(f'magnolia.app called with args {args}')
    logger.info(f'Using profile: {profile}')

    # Application and module self-test
    if args.test:
        import unittest
        import magnolia.tests

        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        suite.addTests(loader.loadTestsFromModule(magnolia))
        runner = unittest.TextTestRunner(verbosity=verbosity)
        runner.run(suite)

    # Application status
    if args.subcommand == 'status':
        print("These config files are loaded:")
        print(f"    {os.path.join(CONFIG_PATH, 'magnolia.cfg')}")
        print(f"    {os.path.join(CONFIG_PATH, 'magnolia_harvests.cfg')}")
        print(f"    {os.path.join(CONFIG_PATH, 'magnolia_scenarios.cfg')}")
        print("XML data path:")
        print(f"    {os.path.abspath(magnolia_config[profile]['InFilePath'])}")
        print("JSON data path:")
        print(f"    {os.path.abspath(magnolia_config[profile]['OutFilePath'])}")
        sys.exit(0)

    #######################
    # Harvest sub-command #
    #######################

    elif args.subcommand == 'harvest':
        write_path = os.path.abspath(magnolia_config[profile]['InFilePath'])
        harvest_parser = configparser.ConfigParser()
        harvest_parser.read(os.path.join(CONFIG_PATH, 'magnolia_harvests.cfg'))

        # Run harvest
        if args.run:
            for section in harvest_parser.sections():
                cli.harvest(harvest_parser[section], section, write_path, verbosity=verbosity)

        # Run harvest selectively by config key
        if args.select:
            try:
                cli.harvest(harvest_parser[args.select], args.select, write_path, verbosity=verbosity)
            except KeyError:
                print(f'The supplied organization key was not found in the config file.\nSupplied key: {args.select}')
                sys.exit(1)

        # Add new harvest config entry
        if args.new:
            cli.new_config_entry(harvest_parser, ['oaiendpoint', 'setlist', 'metadataprefix'],
                                 os.path.join(CONFIG_PATH, 'magnolia_harvests.cfg'))

        # List harvest config entries
        if args.list:
            cli.config_list(harvest_parser)

        # Run harvest interactively
        if args.interactive:
            cli.interactive_run(magnolia_config, harvest_parser, 'harvest', profile, write_path, verbosity=verbosity)

    #########################
    # Transform sub-command #
    #########################

    elif args.subcommand == 'transform':
        scenario_parser = configparser.ConfigParser()
        scenario_parser.read(os.path.join(CONFIG_PATH, 'magnolia_scenarios.cfg'))

        # Output transformation results to console (T/F)
        to_console = False
        if args.to_console:
            to_console = True

        # Run transformation
        if args.run:
            for section in scenario_parser.sections():
                try:
                    cli.transform(magnolia_config, scenario_parser[section], section, profile, verbosity=verbosity,
                                  to_console=to_console)
                except FileNotFoundError:
                    logger.warning(f"No data found for {section}")
                    continue

        # Run transformation selectively by config key
        if args.select:
            try:
                cli.transform(magnolia_config, scenario_parser[args.select], args.select, profile, verbosity=verbosity,
                              to_console=to_console)
            except KeyError:
                print(f'The supplied organization key was not found in the config file.\nSupplied key: {args.select}')
                sys.exit(1)

        # Add new transformation config entry
        if args.new:
            cli.new_config_entry(scenario_parser, ['scenario', 'map', 'dataprovider', 'intermediateprovider'],
                                 os.path.join(CONFIG_PATH, 'magnolia_scenarios.cfg'))

        # List transformation config entries
        if args.list:
            cli.config_list(scenario_parser)

        # Run transformation interactively
        if args.interactive:
            cli.interactive_run(magnolia_config, scenario_parser, 'transform', profile, verbosity=verbosity,
                                to_console=to_console)
