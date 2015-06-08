# -- coding: utf-8 --

# Copyright 2015 Nickolas Whiting
#
# @author  Nickolas Whiting  <prggmr@gmail.com>

from pmpy import PmPyCommand, PATH, command, DEFAULT_CONFIG, pmpy_format, \
    call_command

class OpenProject(PmPyCommand):
    """Opens a project activating the environment and opening using the 
    configured editor.
    """
    
    def get_args(self):
        return [
            [['project'], {
                'help': 'Name of the project',
            }],
        ]

    def __call__(self, args):
        config = self.get_project_config(args.project)
        call_command('load_env', args=args)
        command(pmpy_format(config.get('pmpy', 'editor'), 
                path=PATH, project=args.project))