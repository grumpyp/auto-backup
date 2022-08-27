from flask import Flask, render_template
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
        data = dict()
        with open('./logs.log', 'r+') as logs:
            for n, line in enumerate(logs.readlines()):
                timestamp, status, msg = line.split(' - ')[0], line.split(' - ')[1], line.split(' - ')[2]
                if status == 'WARNING':
                    if "Googledrive" in msg:
                        # improvement: create ahref to googledrive to view with
                        # https://drive.google.com/file/d/<id>/view
                        file_id = msg.split('ID: ')[1]
                        data[n] = [timestamp, status, msg]
                    else:
                        data[n] = [timestamp, status, msg]

                pass
        return render_template('index.html', data=data)


    app.run(host='0.0.0.0', port='80')
