# symplpay

## Introduction

symplpay is a small web app which demonstrates how to combine several highly-related REST API calls on server _A_ into a single REST API call for server _B_. One reason for implementing such a pattern is to make API consumers' lives easier.

### License

This software is distributed under the **MIT License**.

### Dependencies

* _Ubuntu 18.04_, _Ubuntu 20.04_, or the latest-and-greatest release of _Windows 10_. While _symplpay_ may work as-is on other Linux OSVs, all testing was performed against the latest HWE LTS versions of _Ubuntu_ and also _Windows 10_
* 64-bit Python 3.6 or higher
* Python's `requests_oauthlib` 3rd party package. Instructions are given below on installing this which is needed to handle the OAuth 2.0 protocol with the remote server
* (Optional) Python's `gunicorn` 3rd party package. Again, there are instructions below on installation which is only necessary to host the local REST API using HTTPS on Linux

### Known Issues

* The "--ssl" flag doesn't work on Windows 10

## Installation

### Python

* _Ubuntu 18.04/20.04 HWE LTS_: open a _Terminal_ and run `sudo apt install python3`. Verify successful installation by running `python3 --version` -> the reported version needs to be >= 3.6.
* _Windows 10_: [download 64-bit Python 3.9](https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe) and install. Once complete, open a _cmd.exe_ and run `python --version` to ensure the 3.x version of Python appears first in your _%PATH%_.

**IMPORTANT NOTE**: all remaining instructions assume you're running Linux. If not the case, simply substitute "python" for "python3", "pip" for "pip3", and "cmd.exe" for "Terminal" in any commands below.

### Python's `requests_oauthlib` Package

From a _Terminal_:

1. `pip3 install requests_oauthlib`
1. Run `python3 -c "import oauthlib"` to confirm the package was successfully installed -> no output and an exit code of 0 is expected.

### (Optional - for HTTPS support in Linux) Python's `gunicorn` Package

From a _Terminal_:

1. (Ubuntu) `sudo apt install openssl`. Probably unnecessary on most systems, but better safe than sorry;)
1. `pip3 install gunicorn`
1. Run `python3 -c "import gunicorn"` to confirm the package was successfully installed -> no output and an exit code of 0 is expected.
1. **IMPORTANT NOTE**: you **must** supply the "--ssl" parameter to the `python3 -m symplpay.server ...` command in the _Server Initialization Instructions_ below to enable HTTPS. I.e., this does not happen automatically simply because you're on Linux

## Running the Web App

Open a new _Terminal_:

1. `export PYTHONPATH=.` (only if you do not already have Python configured to look in the current directory for Python files)
1. `cd <where-you-dropped-this>/symplpay`
1. Run `python3 -m symplpay.server -h` to see what configurable server parameters are available...
1. `python3 -m symplpay.server --client_id <your ID> --client_secret <your secret> --debug` to start the server
1. Open [http://localhost:8080](http://localhost:8080) (or [https://localhost:8080](https://localhost:8080) if you supplied the "--ssl" flag) in your favorite web browser
1. Use _curl_, _Postman_, etc. to invoke the server's single API, http(s)://localhost:8080/compositeUsers/:userId 