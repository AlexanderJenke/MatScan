from flask import Flask, escape, request, send_from_directory, render_template
import threading
import json

app = Flask(__name__, static_url_path='')
event = threading.Event()


def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


@app.route('/')
def main():
    rows = [{'name': "Test", 'exp': "01.2020", 'count': 5, 'id': "123456789_01.2020"},
            {'name': "Test2", 'exp': "09.2021", 'count': 500, 'id': "234567890_09.2021"},
            {'name': "None", 'exp': "00.0000", 'count': 0, 'id': "0_00.0000"},
            {'name': "None", 'exp': "00.0000", 'count': 0, 'id': "0_00.0000"},
            {'name': "None", 'exp': "00.0000", 'count': 0, 'id': "0_00.0000"},
            {'name': "None", 'exp': "00.0000", 'count': 0, 'id': "0_00.0000"},
            {'name': "None", 'exp': "00.0000", 'count': 0, 'id': "0_00.0000"},
            {'name': "None", 'exp': "00.0000", 'count': 0, 'id': "0_00.0000"},
            {'name': "None", 'exp': "00.0000", 'count': 0, 'id': "0_00.0000"},
            {'name': "None", 'exp': "00.0000", 'count': 0, 'id': "0_00.0000"},
            {'name': "None", 'exp': "00.0000", 'count': 0, 'id': "0_00.0000"},
            {'name': "None", 'exp': "00.0000", 'count': 0, 'id': "0_00.0000"},
            {'name': "None", 'exp': "00.0000", 'count': 0, 'id': "0_00.0000"},
            ]

    # rows = []
    return render_template('page.html', main='main_scan.html', rows=rows)


@app.route('/impressum')
def impressum():
    return render_template('impressum.html')


@app.route('/img/<path:path>')
def images(path):
    return send_from_directory('static/img', path)


@app.route('/webfonts/<path:path>')
def fonts(path):
    return send_from_directory('static/webfonts', path)


@app.route("/css/<path:path>")
def css(path):
    return send_from_directory("static/css", path)


@app.route("/js/<path:path>")
def javascript(path):
    return send_from_directory("static/js", path)


@app.route('/event')
def e():
    print("incomming event")
    event.set()
    return f"thanks!"


s = 0


@app.route('/poll')
def test():
    global s
    # print(request.args.get("state"))
    if event.wait(30.0):
        event.clear()
        print("poll event")
        s += 1
        return json.dumps({'s': 'event',
                           'd': s})
    else:
        print("poll timeouted")
        return json.dumps({'s': ''})


if __name__ == '__main__':
    app.run(
        # host="10.0.0.20",
        # port=5000,
    )
