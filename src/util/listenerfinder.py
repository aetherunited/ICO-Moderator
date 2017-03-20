discovered = []


def register(listener: type):
    """
    Use this as an annotation.
    Add a listener to the discovered listeners list.
    :param listener: the listener class
    :return: the listener, unmodified
    """
    discovered.append(listener)
    return listener


def initialize_discovered():
    out = []
    for listen in discovered:
        out.append(listen())
    return out
