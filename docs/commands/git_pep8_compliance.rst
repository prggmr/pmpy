git_pep8_compliance
___________________

Generates a report on the given project for PEP8 compliance.

    Uses `git blame` for determining who committed the violation.
    

.. code-block:: bash

	usage: pmpy git_pep8_compliance [-h] [--pep8-options PEP8_OPTIONS]
	                                [--blame-options BLAME_OPTIONS]
	                                [--output {csv,json}]
	                                project
	
	positional arguments:
	  project               Name of the project
	
	optional arguments:
	  -h, --help            show this help message and exit
	  --pep8-options PEP8_OPTIONS
	                        pep8 options.
	  --blame-options BLAME_OPTIONS
	                        git blame options.
	  --output {csv,json}   Output format.
	