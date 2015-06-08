create_project
______________

Creates a new project at the given destination x in the projects directory.
    

.. code-block:: bash

	usage: pmpy create_project [-h] [-d] [-f] [-r REPO] [-o] [--no-env]
	                           [--clone CLONE]
	                           project
	
	positional arguments:
	  project               Name of the project
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -d, --delete          Delete project if already exists.
	  -f, --force           Force deletion of the project.
	  -r REPO, --repo REPO  Repository to clone.
	  -o, --open            Automatically run the open_project command.
	  --no-env              Do not create an environment.
	  --clone CLONE         Command to use for cloning.
	