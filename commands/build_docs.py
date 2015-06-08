# -- coding: utf-8 --

# Copyright 2015 Nickolas Whiting
#
# @author  Nickolas Whiting  <prggmr@gmail.com>

# Python
import os, glob, StringIO

# pmpy
from pmpy import PmPyCommand, command, load_command,  AVAILABLE_COMMANDS

class BuildDocs(PmPyCommand):
    """Compiles the command documentation.
    """
    
    def get_args(self):
        return [
            [['output'], {
                'help': 'Output destination',
            }],
        ]

    def __call__(self, args):
        for _command in AVAILABLE_COMMANDS:
            _class = load_command(_command)
            with open('{0}/{1}.rst'.format(args.output, _command), 'w') as _f:
                template = open('build/command_template.txt', 'r')
                template_text = template.read()
                template.close()
                print '{0}/{1}.rst'.format(args.output, _command)
                help_text = "\n".join(["\t{0}".format(x) for x in command(
                    'pmpy {0} -h'.format(_command, '-h'),
                    capture_output=True).split("\n")])

                _f.write(template_text.format(
                    command=_command, command_underline='_'*(len(_command)), 
                    docstring=_class.__doc__, 
                    help_text=help_text))
            with open('{0}/available_commands.rst'.format(args.output, _command), 'w') as _f:
                _f.write("Available commands\n")
                _f.write("------------------\n\n")
                for _c in AVAILABLE_COMMANDS:
                    _f.write(".. include:: commands/{0}.rst\n".format(_c))
