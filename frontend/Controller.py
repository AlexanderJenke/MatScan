import json

from flask import render_template

from core import core


class PageController:
    def poll(self, sid):
        if core.event_bus.wait(sid):
            data = core.event_bus.get(sid)
            if data is not None:
                return json.dumps(data), 200
        return "", 204

    def page(self):
        raise NotImplementedError()

    def event(self, **kwargs):
        raise NotImplementedError()


class CartController(PageController):
    def event(self, **kwargs):
        # handle events
        return "", 200

    def page(self):
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


class PollExampleController(PageController):
    def __init__(self):
        self.s = 0

    def page(self):
        return render_template("poll_example.html", d=self.s)

    def event(self, **kwargs):
        print("incomming event")
        print(kwargs)
        self.s += 1
        core.event_bus.push({'d': self.s})
        return f"thanks!"
