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
            [['--no-editor'], {
                'help': 'Do not open the project in the editor',
                'action': 'store_true',
                'default': False
            }],
            [['--no-load'], {
                'help': 'Do not load the project environment',
                'action': 'store_true',
                'default': False
            }]
        ]

    def __call__(self, args):
        config = self.get_project_config(args.project)
        if not args.no_load:
            call_command('load_env', args=args)
        if not args.no_editor:
            command(pmpy_format(config.get('pmpy', 'editor'), 
                    path=PATH, project=args.project))