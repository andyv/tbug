#!/usr/bin/env python3

import urwid


# The config class contains the state of the configurable things.

class config:
    escape = '`'

    palette = [ ('status',  'black', 'dark red' ), ]

    pass




# status()-- The status line appears at the top and indicates current
# state.

class status(urwid.Text):
    def __init__(self):
        urwid.Text.__init__(self, '')
        return

    def add(self, text):
        self.set_text(text)
        return

    pass


# cmdline()-- The command line is for entering commands.

class cmdline(urwid.Edit):
    def __init__(self, main):
        urwid.Edit.__init__(self, '> ')
        self.main = main
        return

    pass



# top_frame()-- An urwid.Frame that contains everything else.

class top_frame(urwid.Frame):
    def __init__(self):
        self.status = status()
        self.cmdline = cmdline(self)
        self.body = urwid.SolidFill('.')

        st = urwid.AttrMap(self.status, 'status')
        urwid.Frame.__init__(self, self.body, st, self.cmdline, 'footer')
        return


# keypress()-- Intercept global keys.

    def keypress(self, size, key):
        if key == config.escape:
            self.status.add('New Status')
            return None

        return urwid.Frame.keypress(self, size, key)

    pass


main = urwid.MainLoop(top_frame(), palette=config.palette)
main.run()





