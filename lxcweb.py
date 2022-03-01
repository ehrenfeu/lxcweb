from flask import Flask, redirect, url_for, render_template
import json


STATUSFILE = "static/status.json"

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


class MachineStatus():
    def __init__(self, status):
        classmap = {'RUNNING': 'text-success',
                    'STOPPED': 'text-error',
                }
        self.name = status["name"]
        self.state = status["state"]
        self.autostart = status["autostart"]
        self.ipv4 = status["ipv4"]
        self.html_class = classmap.get(self.state, 'text-warning')


def machine_states():
    with open(STATUSFILE, "r", encoding="utf-8") as infile:
        status_json = json.load(infile)
    machines = []
    for machine in status_json["lxc_running"]:
        status = MachineStatus(machine)
        machines.append(status)
    for machine in status_json["lxc_stopped"]:
        status = MachineStatus(machine)
        machines.append(status)
    return machines


def single_machine_state(name):
    machines = machine_states()
    for machine in machines:
        if machine.name == name:
            return machine
    return None


@app.route('/')
def show_container():
    machines = machine_states()
    return render_template('overview.html', machines=machines)

@app.route('/<name>/')
def info(name):
    machine = single_machine_state(name)
    return render_template('details.html', machine=machine)


# @app.route('/<name>/<action>')
# def action(name, action):
#     m = lxc.Container(name)
#     result = getattr(m, action)()
#     if action != "info":
#         return redirect(url_for('show_container'))
#     else:
#         return result
# 
# @app.route('/<name>/delete')
# def deleteMachine(name):
#     m = lxc.Container(name)
#     if m.running:
#         m.stop()
#     m.destroy()
#     return redirect(url_for('show_container'))
# 
# @app.route('/<name>/clone/<newname>')
# def clone(name, newname):
#     m = lxc.Container(name)
#     m.clone(newname)
#     return redirect(url_for('show_container'))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
