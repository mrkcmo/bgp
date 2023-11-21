# Get BGP Routes from Cisco Router, Tabulate Routes, and Write Routes to Result File.

Follow these steps to get started:

1. Verify you are running python 3.9 or above ('python3 --version')
2. Install requirements from 'requirements.txt' file ('python3 -m pip install -r requirements.txt')
3. Run grab_routes.py with the required arguments of 'python3 grab_bgp_routes.py -u Username -d DeviceIP'
4. Enter your password for device login when prompted
5. Script will run and will output to screen and file the results

It is recommended you use VSCode as an IDE and install the "flake8" and "Python" extensions.
With VSCode you can directory open the Git Repository and setup a Python Virtual Environment
which is shown here: https://code.visualstudio.com/docs/python/environments#_creating-environments

You can then follow the steps above to install the requirements into the Python Virtual Environment. 