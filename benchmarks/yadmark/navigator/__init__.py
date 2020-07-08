import inspect

import IPython
from traitlets.config.loader import Config

from .navigator import NavigatorApp,t,o,l


def yelp(*args):
    """
        Help function (renamed to avoid clash of names) - short cut: h.
    """
    if len(args) == 0:
        print(
            f"""Welcome to yadism benchmark skript!
Available short cuts (variables):
    t = "{t}" -> "theor[y|ies]"
    o = "{o}" -> "observable[s]"
    l = "{l}" -> "log[s]"
Available functions (selected list):
    h - this help
    m - change mode
    g - getter
    ls - listing (reduced information)
    p - printing (using ls)
    diff - subtractig logs"""
        )
    elif len(args) == 1:
        return help(*args)
    return None


h = yelp


app = NavigatorApp("sandbox")


def change_mode(*args):
    global app
    return app.change_mode(*args)


m = change_mode


def get(*args):
    global app
    return app.get(*args)


g = get


def p(*args):
    global app
    return app.print(*args)


def ls(*args):
    global app
    return app.list_all(*args)


def subtract_tables(*args):
    global app
    return app.subtract_tables(*args)


diff = subtract_tables


def launch_navigator():
    c = Config()
    banner = """
        Welcome to yadism benchmark skript!
        call yelp() or h() for a brief overview.
    """
    c.TerminalInteractiveShell.banner2 = inspect.cleandoc(banner) + "\n" * 2

    args = """['from yadmark.navigator import *','from yadism import *',]"""

    IPython.start_ipython(
        argv=[f"--InteractiveShellApp.exec_lines={args}", "--pylab",], config=c
    )
