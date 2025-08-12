<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <script src="https://yastatic.net/jquery/2.2.3/jquery.min.js" crossorigin="anonymous"></script>
    <link href="https://yastatic.net/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" crossorigin="anonymous">
    <script src="https://yastatic.net/bootstrap/3.3.6/js/bootstrap.min.js" crossorigin="anonymous"></script>
    <link type="text/css" href="https://yandex.st/highlightjs/8.0/styles/github.min.css" rel="stylesheet"/>
    <script type="text/javascript" src="https://yandex.st/highlightjs/8.0/highlight.min.js"></script>
    <script type="text/javascript" src="https://yandex.st/highlightjs/8.0/languages/bash.min.js"></script>
    <script type="text/javascript" src="https://yandex.st/highlightjs/8.0/languages/json.min.js"></script>
    <script type="text/javascript" src="https://yandex.st/highlightjs/8.0/languages/xml.min.js"></script>
    <script type="text/javascript">hljs.initHighlightingOnLoad();</script>

    <style>
        pre {
            white-space: pre-wrap;
            margin: 5px 0;
        }
        .status-success {
            color: #28a745;
            font-weight: bold;
        }
        .status-error {
            color: #dc3545;
            font-weight: bold;
        }
        .status-info {
            color: #17a2b8;
            font-weight: bold;
        }
        .section-title {
            color: #6c757d;
            margin-top: 15px;
        }
    </style>
</head>
<body>
<div>
    <pre><code>HTTP Response:
{% if response.status_code %}<span class="
{% if response.status_code < 300 %}status-success
{% elif response.status_code < 400 %}status-info
{% else %}status-error
{% endif %}
">{{response.status_code}}</span>{% else %}None{% endif %}
from {% if response.url %}{{response.url}}{% else %}None{% endif %}</code></pre>
</div>

{% if response.headers %}
    <h4 class="section-title">Response Headers</h4>
    <div>
    {% for key, value in response.headers.items() %}
        <div>
            <pre><code><b>{{key}}</b>: {{value}}</code></pre>
        </div>
    {% endfor %}
    </div>
{% endif %}

{% if response.text %}
    <h4 class="section-title">Response Body</h4>
    <div>
        <pre><code>{{response.text}}</code></pre>
    </div>
{% endif %}

{% if response.cookies %}
    <h4 class="section-title">Response Cookies</h4>
    <div>
    {% for key, value in response.cookies.items() %}
        <div>
            <pre><code><b>{{key}}</b>: {{value}}</code></pre>
        </div>
    {% endfor %}
    </div>
{% endif %}

{% if response.elapsed %}
    <h4 class="section-title">Response Time</h4>
    <div>
        <pre><code>{{response.elapsed.total_seconds()}} seconds</code></pre>
    </div>
{% endif %}
</body>
</html>