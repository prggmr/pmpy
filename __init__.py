#!/usr/bin/env python
# -- coding: utf-8 --

# Copyright 2015 Nickolas Whiting
#
# @author  Nickolas Whiting  <prggmr@gmail.com>

__VERSION__ = 0.1

# Python
import argparse
import ConfigParser
import glob
import re
import os
import sys
from importlib import import_module
from subprocess import *

# Configuration

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
DEFAULT_CONFIG = ConfigParser.ConfigParser(allow_no_value=True)
DEFAULT_CONFIG_FILE = '{0}/pmpy.ini'.format(os.path.dirname(os.path.realpath(__file__)))
DEFAULT_CONFIG.readfp(open(DEFAULT_CONFIG_FILE))
USER_CONFIG_FILE = '{0}/.pmpy'.format(os.path.expanduser('~'))
DEFAULT_CONFIG.read(USER_CONFIG_FILE)
PATH = DEFAULT_CONFIG.get('pmpy', 'path')
COMMAND_PATHS = DEFAULT_CONFIG.get('pmpy', 'commands').split(',')
DEFAULT_KWARGS = {
    'pmpy_path': os.path.dirname(os.path.realpath(__file__))
}

# Convert CamelCase to underscore_split
def camel_to_underscore(name):
    """Convert a camel cased string to underscore cased.
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def underscore_to_camel(name):
    """Convert a underscore cased string to camel cased.
    """
    return "".join('{0}{1}'.format(x[0].capitalize(), x[1:]) for x in name.split('_'))

# Command Function
def command(x, capture_output = False, *args, **kwargs):
    """Runs a shell command, optionally capturing the output.
    """
    if capture_output:
        proc = Popen(x, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True, shell=True, *args, **kwargs)
        return proc.stdout.read()
    return str(Popen(x, stdout=sys.stdout, shell=True, *args, **kwargs).communicate()[0])

def pmpy_format(x, default_kwargs = DEFAULT_KWARGS, *args, **kwargs):
    """String formatting function provides a standard set of default arguments.
    """
    return x.format(**dict(DEFAULT_KWARGS.items() + kwargs.items()))

def call_command(command, args):
    """Calls a pmpy command.
    """
    _class = load_command(command)
    return _class(args)

def load_command(command_str):
    """Attempts to import and load a command class.
    """
    _class = getattr(import_module('commands.{0}'.format(command_str)), 
                     underscore_to_camel(command_str))()
    return _class

class PmPyCommand(object):
    """Runs a command.
    """
    help = None

    def get_args(self):
        """Returns a list to be provided to ArgumentParser as a subparser.

        Arguments are expected as [[*[], **{}]].
        """
        raise NotImplemented()

    def __call__(self, args):
        """Runs the command.
        """
        raise NotImplemented()

    def get_project_path(self, project, path=PATH):
        return '{0}/{1}'.format(path, project)

    def get_project_config(self, project, path=PATH):
        """Gets the current projects configuration.

        Uses the default configuration as a base.
        """
        config_file = '{0}/{1}/.pmpy'.format(path, project)
        config = DEFAULT_CONFIG
        if os.path.exists(config_file):
            config.read(config_file)
        return config

# Load available commands
AVAILABLE_COMMANDS = []
for path in COMMAND_PATHS:
    path = pmpy_format(path)
    os.chdir(path)
    for f in glob.glob('*.py'):
        if '__' in f:
            continue
        AVAILABLE_COMMANDS.append(f.replace('.py', ''))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='pmpy', description="Simple python project manager.")
    parser.add_argument('-l', '--list', help='List available commands.', 
                        action='version', 
                        version="Available commands : {0}".format(
                            ", ".join([camel_to_underscore(x) for x in AVAILABLE_COMMANDS])))
    parser.add_argument('-V', '--version', action='version', 
                        version='%(prog)s {0}'.format(__VERSION__))

    sub_commands = parser.add_subparsers(
        title='Available commands', 
        description='Manage command to run. List of available commands.')
    for _c in AVAILABLE_COMMANDS:
        _class = load_command(_c)
        args = _class.get_args()
        sub_parser = sub_commands.add_parser(_c, help=_class.__doc__)
        sub_parser.set_defaults(func=_class)
        for arg in args:
            sub_parser.add_argument(*arg[0], **arg[1])

    # Call the command
    args = parser.parse_args()
    args.func(args)
    