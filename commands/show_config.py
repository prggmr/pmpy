# -- coding: utf-8 --

# Copyright 2015 Nickolas Whiting
#
# @author  Nickolas Whiting  <prggmr@gmail.com>

from pmpy import PmPyCommand, PATH, command, DEFAULT_CONFIG, DEFAULT_CONFIG_FILE

class ShowConfig(PmPyCommand):
    """Dumps the configuration. If given a project it will dump that projects 
    configuration.
    """
    
    def get_args(self):
        return [
            [['project'], {
                'help': 'Optional name of project to show.',
                'nargs': '?'
            }],
            [['section'], {
                'help': 'Optional section to show.',
                'default': 'pmpy',
                'nargs': '?'
            }],
        ]

    def __call__(self, args):
        config_file = '{0}/.pmpy'.format(
            self.get_project_path(args.project)) if args.project else DEFAULT_CONFIG_FILE
        config = self.get_project_config(args.project) if args.project else DEFAULT_CONFIG
        if config is None:
            if args.project:
                print 'Configuration file {0} was not found.'.format('{0}/.pmpy'.format(
                        self.get_project_path(args.project)))
            config_file = DEFAULT_CONFIG_FILE
            config = DEFAULT_CONFIG
        print 'Loaded configuration file {0}'.format(config_file)
        for x,y in config.items(args.section):
            print '{0} = {1}'.format(x, y)