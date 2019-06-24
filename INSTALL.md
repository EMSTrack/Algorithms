# Introduction

**Operating Systems**: We highly recommend using a UNIX-based operating system like Mac OS or Linux. Windows is okay, if you put in extra work. We're working on containerizing the simulation using Docker, but there is currently no guarantees there. 

**Programming Language**: The latest version of Python works well, though slightly older versions will also work fine. Your mileage may vary. 

## Suggested operating systems: 

### UNIX-based

- Ubuntu 16 or higher
- Mac OS Sierra or higher

### Windows 10 

- Best: use one of Microsoft's Linux subsystems to install Linux bash (such as Ubuntu 16 or 18.) 
- Easiest: Install Docker and run our build which uses the Ubuntu 18 base. Warning: developers should use the above Linux bash option instead. 


## Programming language: 
- Python 3. At least Python 3.5 should be good.
- Python 2 will not work.
- Suggested: Python 3.7 by installing python3 from brew or apt-get. 


### Libraries

Install the dependencies via the following command:

`python3 -m pip3 install -r requirements.txt` 

## Run

If all is well, the simulator library should be runnable now. If you get a help message by running the below command, the basic installation is complete. 

`python3 run-simulation --help`

## A virtual environment (optional)

Create a new environment with Python 3: 

`virtualenv -p python3 venv`

Use the new environment:

`source venv/bin/activate`

