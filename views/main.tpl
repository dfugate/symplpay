% include('header.tpl', title='SymplPay - Home')

<h1>
    Home
</h1>
<hr />

<div class="well">
    <p>
    <i>symplpay</i> is a small web app
    <a onclick="window.open('http://www.linkedin.com/in/davidfugate');return false;" style="cursor: pointer;">I</a> wrote
    which  demonstrates how to combine several highly-related REST API calls on server <i>A</i> into a single REST API call for 
    server <i>B</i>. One reason for implementing such a pattern is to make API consumers' lives easier.
    <br/>
    It's open source and the full source code as was as complete documentation is available on my
    <a onclick="window.open('https://github.com/dfugate/symplpay'); return false;" style="cursor: pointer;">
    GitHub account</a>.
    </p>
</div>

% include('footer.tpl')