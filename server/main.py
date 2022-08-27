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
        dates = []
        log_type = []
        msgs = []
        data = {'dates': dates, 'log_types': log_type, 'msgs': msgs}
        with open('./logs.log', 'r+') as logs:
            for line in logs.readlines():
                date, status, msg = line.split(' - ')[0], line.split(' - ')[1], line.split(' - ')[2]
                dates.append(date)
                log_type.append(status)
                msgs.append(msg)
        
        print(dates)
        print(log_type)
        print(msgs)

        return render_template('index.html', data=data)


    app.run(host='0.0.0.0', port='80')
