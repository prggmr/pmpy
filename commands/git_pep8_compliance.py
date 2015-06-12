# -- coding: utf-8 --

# Copyright 2015 Nickolas Whiting
#
# @author  Nickolas Whiting  <prggmr@gmail.com>

from pmpy import PmPyCommand, PATH, command, DEFAULT_CONFIG, pmpy_format, \
    call_command

# Python
from collections import defaultdict
import re
import json
import csv
import sys

class GitPep8Compliance(PmPyCommand):
    """Generates a report on the given project for PEP8 compliance.

    Uses `git blame` for determining who committed the violation.
    """
    
    def get_args(self):
        return [
            [['project'], {
                'help': 'Name of the project',
            }],
            [['--pep8-options'], {
                'help': 'pep8 options.'
            }],
            [['--blame-options'], {
                'help': 'git blame options.'
            }],
            [['--output'], {
                'help': 'Output format.',
                'default': 'csv',
                'choices': ['csv', 'json']
            }],
        ]

    def __call__(self, args):
        config = self.get_project_config(args.project)
        pep8 = command('pep8 {path}/{project} {pep8_options}'.format( 
                path=PATH, project=args.project, pep8_options=args.pep8_options), 
                    capture_output=True)
        if '-h' in args.pep8_options or '--help' in args.pep8_options:
            print pep8
            return
        blame = None
        current_file = None
        authors = {}
        git_blame_regex = re.compile(ur"([\^\w\d]{8})(.*)\(([\w\s]+?|\<.*\>)[\s]+([0-9\-\s:\+]+)\s{1}([0-9]+)\)(.*)")
        for line in pep8.split("\n"):
            if line == '.':
                continue
            try:
                _file, _error, _desc = line.split(" ", 2)
            except Exception, e:
                print "Error checking line {0}. Error {1}".format(line, e)
                continue
            _file, _line, _column, _blank = _file.split(':', 3)
            blame_command = 'cd {path}/{project} && git blame {file} -L {line},{line} {blame_options}'.format(
                path=PATH, project=args.project, file=_file, line=_line, blame_options=args.blame_options)
            blame = command(blame_command, capture_output=True)
            blame_data = git_blame_regex.search(blame)
            if blame_data is None:
                if 'fatal: no such path' in blame:
                    continue
                else:
                    print "Error checking blame {0}".format(blame)
                continue
            _commit = blame_data.group(1)
            _author = blame_data.group(3)
            _date = blame_data.group(4)
            if _author not in authors:
                authors[_author] = {
                    'files': {},
                    'commits': [],
                    'error_count': 0
                }
            authors[_author]['error_count'] += 1
            if _commit not in authors[_author]['commits']:
                authors[_author]['commits'].append(_commit)
            if _file not in authors[_author]['files']:
                authors[_author]['files'][_file] = []
            authors[_author]['files'][_file].append({
                'line': _line,
                'column': _column,
                'error': _desc,
                'errorno': _error
            })
        if args.output == 'json':
            print json.dumps(authors)
        if args.output == 'csv':
            writer = csv.writer(sys.stdout)
            writer.writerow(['Author', 'Errors', 'Files'])
            for author, error_data in authors.iteritems():
                file_errors = []
                for _f, _f_data in error_data['files'].iteritems():
                    errors = _f.replace(' {path}/{project}'.format(path=PATH, project=args.project), 
                                        '')
                    errors += "\n".join(["\tLine : {0} Error : {1}".format(x['line'], x['error']) \
                                         for x in _f_data])
                    file_errors.append(errors)
                writer.writerow([author, error_data['error_count'], "\n".join(file_errors)])