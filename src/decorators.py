import asyncio


def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

    return wrapped


def constant(f):
    def fset(self, value):
        raise TypeError

    def fget(self):
        return f()
    return property(fget, fset)
