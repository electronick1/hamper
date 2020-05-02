from functools import wraps


class Command:

    entry_method = "run"
    post_entry = "__post_run__"

    def __init__(self, handler):
        self.handler = handler

    def init_entry_method(self):
        """
        Replacing `entry_method` by wrapper, which is able to call __post_entry__
        method afterwards.
        """
        entry_method = getattr(self.handler, self.entry_method, default=None)
        if entry_method is None:
            return

        entry_method = self.entry_method_decorator(entry_method)

        setattr(self.handler, self.entry_method, entry_method)

    def entry_method_decorator(self, method):
        """Wraps `entry_method` to call another function afterwards"""
        @wraps(method)
        def wrap(command_self, *args, **kwargs):
            result = method(*args, **kwargs)

            post_entry = getattr(command_self, self.post_entry, default=None)
            if post_entry:
                post_entry(result)

            return result

        return wrap


class AttrsCommand(Command):
    pass
