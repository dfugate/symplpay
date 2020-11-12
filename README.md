# symplpay

# Disclaimer

THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL INOMALY LLC
OR ANY OF IT'S CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.

# Prerequisites to Running this Web App

## Install Python

* Ubuntu 18.04/20.04 HWE LTS: open an _xterm_ and run `sudo apt-get install python3`. Verify the install by running `python3 --version` - the reported version needs to be >= 3.6.
* Windows 10: [download](https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe) and install 64-bit Python 3.9. Once complete, open a _cmd.exe_ and run `python --version` to ensure the 3.9 version of Python appears first in your _%PATH%_.

**IMPORTANT NOTE**

All remaining instructions below assume you're running Linux instead of Windows. If this is not the case, simply substitute "python" for "python3", "pip" for "pip3", and "cmd.exe" for "xterm" in any commands below.

## Install Python's requests_oauthlib Package

1. Open an _xterm_ and run `pip3 install requests_oauthlib`
2. Run `python3 -c "import oauthlib"` to confirm the package has been successfully installed. No output and an exit code of 0 is expected.

# Server Initialization Instructions
Open a new _xterm_:
1. `export PYTHONPATH=.` (only if you do not already have Python configured to look in the current directory for Python files)
1. `python3 -m symplpay.server --client_id <your ID> --client_secret <your secret> --debug` to start the server. You can also run `python3 symplpay/server` to see the many configurable server parameters
1. Open [http://localhost:8080](http://localhost:8080) in your favorite web browser
1. Use _curl_, _Postman_, etc. to invoke the server's single API - http://localhost:8080/compositeUsers/:userId