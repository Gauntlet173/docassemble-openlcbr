# docassemble-openlcbr
A docassemble package for case outcome prediction using the analogical reasoning features of openlcbr.
##Requirements
* docassemble
* openlcbr
* Python 3.6 (required by openlcbr)
## Installation Procedure
Note that this is not a final installation procedure for the package, this just gets you as far as development has gone so far.
For the time being, docassemble-openlcbr is expecting OpenLCBR to be installed at /opt/openlcbr inside the docker container for docassemble.
* On the machine running the docassemble docker container, run the docker command to find the container.
* Run `docker -it [container ID] /bin/bash` to start a bash shell "inside" the docker container.
* Once inside the docker container, `cd /opt` and then `git clone https://github.com/mgrabmair/openlcbr`
* In /opt/openlcbr run `python3 lcbr.py data/trade-secret-cases.yaml` to see if openlcbr is running properly.
* to be continued ...
## Current Issues:
* Docassemble is written in Python 2, and OpenLCBR is written in Python 3. Either it needs to be re-written as a Python 2 package, or we need to call it from a docassemble package using a subprocess call.  For the time being, I'm going with the latter, but things would be a little smoother if we could convert it.
* Currently, OpenLCBR will not run from the command line within the Docker container for docassemble. I'm thinking it's probably a python versioning problem.
## Progress:
* Figured out how to import python modules into docassemble packages to be able to make calls to other executables on the container.
* Figured out how to display the output of a call to an executable in a docassemble interview.
* Figured out how to install openlcbr inside a docassemble docker container.
## Work Plan
* Get OpenLCBR running inside docassemble container
* Get output of OpenLCBR test data displayed on docassemble interview
* Have DocAssemble interview generate a case file to test against the database.
* Reformat openlcbr explanation output as structured data
* Display explanation data in docassemble interview
