
class TransportBase:

    def __init__(self, event_manager):
        pass

    def send(self, event_hook, obj):
        raise NotImplementedError()

    def register(self, event_hook):
        raise NotImplementedError()
