# -- coding: utf-8 --

# Copyright 2015 Nickolas Whiting
#
# @author  Nickolas Whiting  <prggmr@gmail.com>

# Python
import sys,os,shutil,ConfigParser

# pmpy
from pmpy import PmPyCommand, PATH,DEFAULT_CONFIG,command

class CreateConfig(PmPyCommand):
    """Creates a new configuration.
    """

    def get_args(self):
        return [
            [['project'], {
                'help': 'Project to create the config for.',
            }],
        ]

    def __call__(self, args):
        config = ConfigParser.ConfigParser(allow_no_value=True)
        config.add_section('pmpy')
        default_config = [
            ('path', self.get_project_path(args.project)),
            ('editor', DEFAULT_CONFIG.get('pmpy', 'editor')),
            ('source', DEFAULT_CONFIG.get('pmpy', 'source')),
            ('clone', DEFAULT_CONFIG.get('pmpy', 'clone')),
            ('env_path', DEFAULT_CONFIG.get('pmpy', 'env_path')),
            ('env_activate_path', DEFAULT_CONFIG.get('pmpy', 'env_activate_path')),
        ]
        for option in default_config:
            input = raw_input('{0} [{1}]: '.format(option[0], option[1]))
            if input is not None:
                config.set('pmpy', option[0], input)
        config.write(open('{0}/.pmpy'.format(self.get_project_path(args.project), 'w+')))