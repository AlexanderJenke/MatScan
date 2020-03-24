import threading

POLL_TIMEOUT = 30.0  # long pool timeout in seconds


class EventBus:
    """
    An EventBus.
    Long poll web calls can subscribe and wait for events using wait(sid)
    Events can be pushed to the Bus using push(data).
    Pushed events can be received by the poll using get(sid)
    """

    def __init__(self):
        self.subscribers = {}  # keys:session ids; values:threading Events for polls to wait with
        self.data = {}  # keys: session ids; values: data objects of events
        self.sub_lock = threading.Lock()
        self.data_lock = threading.Lock()

    def wait(self, sid):
        """
        poll waits for update using the event object connected to its session id
        if the session id is new an event object is created
        :param sid: session id
        :return: true if new event occured, false if timeout occured
        """
        with self.sub_lock:
            if sid not in self.subscribers:
                self.subscribers[sid] = threading.Event()
            event = self.subscribers[sid]
        return event.wait(POLL_TIMEOUT)

    def push(self, data):
        """
        push a new event into the bus and notify all subscribed polls
        :param data: the events data object, is handed over to the poll
        """
        with self.sub_lock:
            for sid in self.subscribers.keys():
                with self.data_lock:
                    if sid not in self.data:
                        self.data[sid] = []
                    self.data[sid].append(data)
                self.subscribers[sid].set()

    def get(self, sid):
        """
        recieve the first event data. This should be called after wait(sid) returned true.
        :param sid: session id
        :return: first event data object, if no event was pushed None is returned
        """
        with self.data_lock:
            try:
                data = self.data[sid].pop(0)
            except IndexError:
                data = None

            if not len(self.data[sid]):
                self.subscribers[sid].clear()
            return data
