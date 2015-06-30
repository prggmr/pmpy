# -- coding: utf-8 --

# Copyright 2015 Nickolas Whiting
#
# @author  Nickolas Whiting  <prggmr@gmail.com>

# Python
import time
import os

# pmpy
from pmpy import PmPyCommand, PATH, command, DEFAULT_CONFIG, pmpy_format

class LoadEnv(PmPyCommand):
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
        kwargs = {
            'path':PATH, 
            'env':env_path, 
            'project':args.project
        }
        tmp_file = "/tmp/pmpy_load_env_{0}".format(str(int(time.time())))
        source = pmpy_format(config.get('pmpy', 'source'), **kwargs)
        source_command = pmpy_format(config.get('pmpy', 'source_command'), **kwargs)
        tmp_file_object = open(tmp_file, 'w+')
        tmp_file_object.write(source)
        tmp_file_object.close()
        command('chmod +x {0}'.format(tmp_file))
        command("{0} {1}".format(source_command, tmp_file))
        os.remove(tmp_file)