# -- coding: utf-8 --

# Copyright 2015 Nickolas Whiting
#
# @author  Nickolas Whiting  <prggmr@gmail.com>

from pmpy import PmPyCommand, PATH, command, DEFAULT_CONFIG, pmpy_format

class CreateEnv(PmPyCommand):
    """Loads a project environment.
    """
    
    def get_args(self):
        return [
            [['project'], {
                'help': 'Name of the project',
            }],
        ]

    def __call__(self, args):
        config = self.get_project_config(args.project)
        if config is None:
            config = DEFAULT_CONFIG
        full_path = '{0}/{1}'.format(PATH, args.project)
        env_path = '{0}/{1}'.format(full_path,
            pmpy_format(config.get('pmpy', 'env_activate_path'), 
                        env_path=config.get('pmpy', 'env_path')))
        command('cd {0} && virtualenv {1}'.format(
                    full_path, DEFAULT_CONFIG.get('pmpy', 'env_path')))
        command(pmpy_format(config.get('pmpy', 'source'), 
                path=PATH, env=env_path, project=args.project))