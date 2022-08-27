from flask import Flask
import logging
log = logging.getLogger('werkzeug')
log.disabled = True

def start():
    import sys
    import click

    cli = sys.modules['flask.cli']

    # put your own message here
    cli.show_server_banner = lambda *x: click.echo("Your logs and backup statistics will be visualized here: http://0.0.0.0")

    app = Flask(__name__)

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"


    app.run(host='0.0.0.0', port='80')
