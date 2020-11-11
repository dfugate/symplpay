% include('header.tpl', title='SymplPay - Home')

<h1>
    Home
</h1>
<hr />

<div class="well">
    <p>
    <i>SymplPay</i> is a small tool
    <a onclick="window.open('http://www.linkedin.com/in/davidfugate');return false;" style="cursor: pointer;">I</a> wrote
    which consolodites several RESTful API calls into one. It is open source and the full source code is available on my
    <a onclick="window.open('https://github.com/dfugate/symplpay'); return false;" style="cursor: pointer;">
    GitHub account</a>.
    </p>
</div>

<div class="well">
    <h4>Key Features</h4>
    <ul>
        <li>Server configuration parameters settable from the command-prompt. Simply
        run "python symplpay/server.py -h" for the list of available arguments.</li>
        <li>Virtually everything is logged – both server and client. See the <a href="/logs">“Logs”</a> page!</li>
    </ul>

    <h4>Technologies</h4>
    <ul>
        <li>Powered by 64-bit Python 3.8</li>
        <li>Tested against both Windows 10 and Ubuntu 18.04</li>
        <li>Server’s web front-end uses the lightweight <i>bottle</i>  framework in conjunction with
            Bootstrap.
        </li>
        <li>Uses Python's <i>requests_oauthlib</i> package to handle authentication. Install via `pip install requests_oauthlib`</li>
    </ul>

</div>

% include('footer.tpl')