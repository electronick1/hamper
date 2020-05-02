import inspect


def event_post_init(event_instance, *args, **kwargs):
    event_instance.__post_init__(event_instance, *args, **kwargs)

    event = event_instance.__event__
    for command in event.commands:
        command.send(event_instance)


class Event:
    def __init__(self, message_class, event_manager):
        self.message_class = message_class
        self.event_manager = event_manager

        self.commands = [
            EventCommand(command, self) for command in message_class.__commands__
        ]

        self.validate_commands()

    def validate_commands(self):
        commands_key = set()
        for command in self.commands:
            command_key = command.get_key()
            base_key = command.get_manager_key()
            if command_key in commands_key:
                raise RuntimeError(
                    "Duplicate command name `%s` for events manager %s"
                    % (command_key, base_key)
                )
            commands_key.add(command_key)


class EventCommand:
    def __init__(self, command, event):
        self.command = command
        self.event = event
        self.app = self.get_app(command)

    def __call__(self, *args, **kwargs):
        return self.command(*args, **kwargs)

    def send(self, data):
        self.event.event_manager.send_message(self, data)

    def get_key(self):
        if hasattr(self.command, "__qualname__"):
            name = self.command.__qualname__
        else:
            name = self.__name__

        return "%s:%s" % (self.app.package_name, name)

    def get_manager_key(self):
        return self.event.event_manager.name

    def get_app(self, command):
        if not inspect.ismethod(command):
            if hasattr(command, "__app__"):
                return command.__app__

            raise RuntimeError(
                "Command from event manager is not `method` or do not have __app__ "
                "defined, see more information in inspect.method. Command name: "
                "%s" % command.__name__
            )

        if not hasattr(command.__self__, "__app__"):
            raise RuntimeError(
                "__app__ is not found for command. Command name: %s" % command.__name__
            )

        return command.__self__.__app__
