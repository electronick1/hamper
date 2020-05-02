import attr
import pkgutil
import sys

from hamper.core.command import AttrsCommand


class App:

    def __init__(self, package_name):
        self.package_name = package_name

        self.commands = []

    def limit_modules(self, keep_public=None):
        package = sys.modules[self.package_name]
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
            if keep_public and modname in keep_public:
                continue
            setattr(package, modname, NotImplemented)

    def attrs_command(self, *args, **kwargs):

        def wrap(callable_obj):
            callable_obj = attr.s(args, **kwargs)(callable_obj)
            callable_obj.__app__ = self

            self.commands.append(AttrsCommand(callable_obj))
            return callable_obj

        return wrap
