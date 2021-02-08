Maybe a submission template
====

## Setup
1. Run `bash setup.sh`
2. To start server, run `start_server.sh`

## Creating a submission
1. Put main python code in `main.py`
2. Put any extra setup steps in `custom_setup.sh`
   1. For example, to install from some requirements.txt `custom_setup.sh` may look like:
    ```
        python -m pip install -r requirements.txt
    ```
