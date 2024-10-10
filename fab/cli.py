import logging

class FabCli():
    """
    Fab command line
    """
    def __init__(self, **kwargs):
        self.loglevel = 'info'
        self.log_format = '%(asctime)19s - %(levelname)8s - %(message)s'
        self.log_datefmt = '%d-%m-%Y %H:%M:%S'
        self.logmap = {
            'info': logging.INFO,
            'warning': logging.WARN,
            'warn': logging.WARN,
            'debug': logging.DEBUG
        }
        final_config = {**self._cmdargs(), **kwargs}
        for k in final_config:
            setattr(self, k, final_config[k])
        self._basic_logging()
        self.loglevel = self.log_level
        self.set_loglevel(self.loglevel)

    def _basic_logging(self):
        logging.basicConfig(level=self.logmap[self.loglevel],
                            format=self.log_format,
                            datefmt=self.log_datefmt)

    def set_loglevel(self, level):
        logging.getLogger().setLevel(self.logmap[level])
        logging.debug('DEBUG mode is enabled')

    def _cmdargs(self):
        """
        Parse command line arguments and read config files (if module exists)
        """
        description = 'Fast Assembly Bootc'
        try:
            import configargparse
            parser = configargparse.ArgParser(
                default_config_files=[
                    'fab.config',
                    '/etc/fab/config',
                    '~/.config/fab/config'],
                description=description
            )
        except ModuleNotFoundError:
            logging.debug('Could not find module "configparse"')
            import argparse
            parser = argparse.ArgumentParser(
                description=description
                )

        parser.add_argument('--log-level', '--loglevel',
                            choices=self.logmap.keys(),
                            type=str.lower,
                            default=self.loglevel,
                            help='Logging level',
                            )
        parser.add_argument('--log-format',
                            type=str,
                            default=self.log_format,
                            help='Python Logger() compatible format string')
        parser.add_argument('--log-datefmt',
                            type=str,
                            default=self.log_datefmt,
                            help='Python Logger() compatible date format str')

        subparsers = parser.add_subparsers(dest='command')
        subparsers.required = False

        try:
            import argcomplete
            from os.path import basename
            parser.add_argument('--bash-completion',
                                action='store_true',
                                help='Dump bash completion file.'
                                ' Activate with "eval '
                                '$({} --bash-completion)"'.format(basename(__file__)))
            argcomplete.autocomplete(parser)
        except ModuleNotFoundError:
            logging.debug('argcomplete module not found, no bash completion available')

        args = parser.parse_args()
        if 'bash_completion' in args:
            if args.bash_completion:
                print(argcomplete.shellcode(basename(__file__), True, 'bash'))
        return vars(args)
