import json
import uuid

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


class CartController(PageController):
    def send_cart_rows(self):
        core.event_bus.push({'action': 'setInnerHTMLById',
                             'values': {
                                 'id': 'cart_tbody',
                                 'content': render_template("cart_tbody_template.html",
                                                            rows=core.cart.get_rows())
                             }})

    def send_alert(self, text, type="warning", timeout=None):

        u = uuid.uuid4().hex
        core.event_bus.push({'action': 'alert',
                             'values': render_template('alert_template.html',
                                                       content=text,
                                                       type=type,
                                                       uuid=u),
                             'timeout': timeout,
                             'uuid': u,
                             })

    def event(self, **kwargs):
        # handle events
        actions = []
        if 'action' in kwargs:
            actions = kwargs['action']

        # handle actions
        if 'get_cart' in actions:
            self.send_cart_rows()

        if 'delete' in actions:
            for mid in kwargs['id']:
                core.cart.del_item(mid)
            self.send_cart_rows()

        if 'set_count' in actions:
            for mid in kwargs['id']:
                try:
                    c = int(kwargs['value'][0])
                    if c < 1:
                        c = 1
                    core.cart.set_count(mid, c)
                except ValueError:
                    self.send_alert(f"'{kwargs['value'][0]}' is not a valid number!", type="info", timeout=5000)

            self.send_cart_rows()

        if 'increase' in actions:
            for mid in kwargs['id']:
                try:
                    core.cart.increase(mid)
                except OverflowError:
                    print("error")
            self.send_cart_rows()

        if 'decrease' in actions:
            for mid in kwargs['id']:
                core.cart.decrease(mid)
            self.send_cart_rows()

        if 'clear_cart' in actions:
            core.cart.clear()
            self.send_cart_rows()

        if 'create' in actions:
            core.cart.add(pzn=uuid.uuid4().hex)
            self.send_cart_rows()

        if 'fill_modal' in actions:
            mid = kwargs['id'][0]
            pzn = mid.split('_')[0]
            core.event_bus.push({'action': 'fill_modal',
                                 'values': render_template("dateModal_template.html",
                                                           name=core.cart.get_item(mid)['name'],
                                                           rows=core.cart.get_dates(pzn))
                                 })

        if 'show_modal' in actions:
            core.event_bus.push({'action': 'show_modal'})


        return "", 200

    def page(self):
        return render_template('page.html', main='content_cart.html')
