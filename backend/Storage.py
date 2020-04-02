class Storage:
    def __init__(self):
        self.items = {}
        pass

    def __getitem__(self, pzn):
        return "Medikament XYZ", {202011: 5, 202012: 5, 202201: 20, 202010: 10}
