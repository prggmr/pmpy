# -- coding: utf-8 --

# Copyright 2015 Nickolas Whiting
#
# @author  Nickolas Whiting  <prggmr@gmail.com>

# Python
import sys,os,shutil

# pmpy
from pmpy import PmPyCommand, PATH,DEFAULT_CONFIG,command

class CreateProject(PmPyCommand):
    """Creates a new project at the given destination x in the projects directory.
    """

    def get_args(self):
        return [
            [['project'], {
                'help': 'Name of the project',
            }],
            [['-d', '--delete'], {
                'help': 'Delete project if already exists.',
                'action': 'store_true',
                'default': False
            }],
            [['-f', '--force'], {
                'help': 'Force deletion of the project.',
                'action': 'store_true',
                'default': False
            }],
            [['-r', '--repo'], {
                'help': 'Repository to clone.',
            }],
            [['-o', '--open'], {
                'help': 'Automatically run the open_project command.',
                'default': False,
                'action': 'store_true',
            }],
            [['--no-env'], {
                'help': 'Do not create an environment.',
                'action': 'store_true',
                'default': False
            }],
            [['--clone'], {
                'help': 'Command to use for cloning.',
                'default': DEFAULT_CONFIG.get('pmpy', 'clone')
            }],
        ]

    def __call__(self, args):
        name = args.project
        full_path = "{0}/{1}".format(PATH, name)
        if os.path.exists(full_path):
            if args.delete:
                shutil.rmtree(full_path, ignore_errors=args.force)
            else:
                print "Project {0} already exists. Use -d to delete.".format(full_path)
                sys.exit(2)

        command('mkdir {0}'.format(full_path))

        if not args.no_env:
            command('cd {0} && virtualenv {1}'.format(
                    full_path, DEFAULT_CONFIG.get('pmpy', 'env_path')))

        if args.open:
            call_command('open_project', args=args)

        if args.repo:
            command(args.clone.format(path=PATH, repo=args.repo, project=name))