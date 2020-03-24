from core.Cart import Cart, Item
from core.EventBus import EventBus
from backend.Storage import Storage

class Core:
    event_bus = EventBus()
    page_controller = None
    cart = Cart()
    storage = Storage()

    # cart.add(Item(1, "Ibu", 0000, 0))
    # cart.add(Item(1, "", 2020, 3))
    # cart.add(Item(1, "", 2021, 1))
    # cart.add(Item(1, "", 2021, 10))
