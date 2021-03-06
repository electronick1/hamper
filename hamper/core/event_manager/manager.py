import attr

from hamper.core.event_manager.event import Event, event_post_init


class EventsManager:

    def __init__(self, name, transport=None):
        self.name = name

        self.events = []
        self.transport = transport(self)

    def attr_event(self, *args, **kwargs):

        def wrap(message_class):
            event = Event(message_class, self)

            message_class.run = event_post_init
            attrs_event = attr.s(*args, **kwargs)(message_class)

            attrs_event.__event__ = event
            attrs_event.__json__ = lambda self: attr.asdict(self)

            self.register_event(event)

            return attrs_event

        return wrap

    def register_event(self, event):
        self.events.append(event)

        for command in event.commands:
            self.transport.register(command)

    def send_message(self, event_hook, data):
        self.transport.send(event_hook, data)
