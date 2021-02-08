Maybe a submission template
====

## Setup
1. Pull in template repo with `git clone --recursive -b test-submission-template --single-branch git@github.com:real-itu/Evocraft-py.git`
2. Run `bash setup.sh`
3. To start server, run `bash start_server.sh`

## Creating a submission
1. Put main python code in `main.py`
2. Put any extra setup steps in `custom_setup.sh`
   1. For example, to install from some requirements.txt `custom_setup.sh` may look like:
    ```
        python -m pip install -r requirements.txt
    ```
