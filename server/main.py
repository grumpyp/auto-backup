from flask import Flask, render_template, send_from_directory
import logging
import sys

import click


log = logging.getLogger('werkzeug')
log.disabled = True


def start():

    cli = sys.modules['flask.cli']

    # put your own message here
    cli.show_server_banner = lambda *x: click.echo("Your logs and backup statistics will be visualized here: http://0.0.0.0:5000")

    app = Flask(__name__)

    @app.route("/")
    def logging_management():
        data = {}
        with open('./logs.log', 'r+') as logs:
            for n, line in enumerate(logs.readlines()):
                timestamp, status, msg = line.split(' - ')[0], line.split(' - ')[1], \
                line.split(' - ')[2]
                if status == 'WARNING':
                    if "Googledrive" in msg:
                        # improvement: create ahref to googledrive to view with
                        # https://drive.google.com/file/d/<id>/view
                        data[n] = [timestamp, status, msg]
                    else:
                        data[n] = [timestamp, status, msg]

                pass
        return render_template('index.html', data=data)

    @app.route("/file/<path:filename>")
    def serve_file(filename):
        print(filename)
        return send_from_directory('storage', filename, as_attachment=True)

    @app.route("/share", methods=["POST"])
    def share():
        data = request.get_json(force=True)




    app.run(host='0.0.0.0', port='5000')
