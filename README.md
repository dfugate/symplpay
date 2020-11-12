# symplpay

# Disclaimer

THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL INOMALY LLC
OR ANY OF IT'S CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.

# Prerequisites

## Install Python

* Ubuntu 18.04/20.04 HWE LTS: open a _Terminal_ and run `sudo apt install python3`. Verify the install by running `python3 --version` - the reported version needs to be >= 3.6.
* Windows 10: [download](https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe) and install 64-bit Python 3.9. Once complete, open a _cmd.exe_ and run `python --version` to ensure the 3.9 version of Python appears first in your _%PATH%_.

**IMPORTANT NOTE**

All remaining instructions assume you're running Linux instead of Windows. If this is not the case, simply substitute "python" for "python3", "pip" for "pip3", and "cmd.exe" for "Terminal" in any commands below.

## Install Python's `requests_oauthlib` Package

From a _Terminal_:

1. `pip3 install requests_oauthlib`
1. Run `python3 -c "import oauthlib"` to confirm the package has been successfully installed. No output and an exit code of 0 is expected.

## (Optional) Install Python's `gunicorn` Package for HTTPS Support in Linux

From a _Terminal_:

1. If you're running Ubuntu, `sudo apt install openssl`. Probably unnecessary on most systems, but better safe than sorry.
1. `pip3 install gunicorn`
1. Run `python3 -c "import gunicorn"` to confirm the package has been successfully installed. No output and an exit code of 0 is expected.
1. **IMPORTANT NOTE**: you'll need to supply the "--ssl" parameter to the `python3 -m symplpay.server ...` command in the _Server Initialization Instructions_ to actually enable HTTPS. I.e., does not happen automatically simply because you're on Linux

# Server Initialization Instructions

Open a new _Terminal_:

1. `export PYTHONPATH=.` (only if you do not already have Python configured to look in the current directory for Python files)
1. `cd <where-you-dropped-this>/symplpay`
1. Run `python3 -m symplpay.server -h` to see what configurable server parameters are available...
1. `python3 -m symplpay.server --client_id <your ID> --client_secret <your secret> --debug` to start the server
1. Open [http://localhost:8080](http://localhost:8080) (or [https://localhost:8080](https://localhost:8080) if you supplied the "--ssl" flag) in your favorite web browser
1. Use _curl_, _Postman_, etc. to invoke the server's single API, http(s)://localhost:8080/compositeUsers/:userId 