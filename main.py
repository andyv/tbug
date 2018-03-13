#!/usr/bin/env python3

import urwid


# The config class contains the state of the configurable things.

class config:
    escape = '`'

    palette = [ ('status',  'black', 'dark red'   ),
                ('splash',  'white', 'dark blue'  ),
                ]


# Translates key names to escape command names.

    esc_cmds = {


        }



    pass




# status()-- The status line appears at the top and indicates current
# state.

class status(urwid.Text):
    def __init__(self):
        urwid.Text.__init__(self, '')
        esc_status = False        
        return


    def generate(self):
        text = ''
        if self.esc_status:
            text += 'ESCAPE'

        else:
            text += 'Ready'
            pass

        self.set_text(text)
        return


    def set_esc_status(self, status):
        self.esc_status = status
        self.generate()
        return

    pass


# cmdline()-- The command line is for entering commands.

class cmdline(urwid.Edit):
    def __init__(self, main):
        urwid.Edit.__init__(self, '> ')
        self.main = main
        return

    pass


class splash(urwid.WidgetWrap):
    signals = [ 'close' ]

    def __init__(self):
        text = ('TBUG, the terminal debugger\n' +
                '(C) 2018 Andy Vaught\n\n' +
                'Press F1 for help')

        lines = text.split('\n')
        width = max(map(len, lines))
        height = len(lines)

        splash = urwid.Text(text, align='center')
        button = urwid.Button('Close')

        urwid.connect_signal(button, 'click',
                             lambda button: self._emit('close'))

        splash = urwid.Pile([ splash, urwid.Text(''), button ])

        splash = urwid.Filler(splash)
        splash = urwid.LineBox(splash)
        splash = urwid.AttrMap(splash, 'splash')

        super().__init__(splash)

        self.splash_width = width + 4
        self.splash_height = height + 4
        return

    pass



# top_frame()-- An urwid.Placeholder that contains everything else.

class top_frame(urwid.PopUpLauncher):
    def __init__(self, main):
        self.main = main
        self.status = status()
        self.cmdline = cmdline(self)
        self.body = urwid.SolidFill('.')

        st = urwid.AttrMap(self.status, 'status')
        top = urwid.Frame(self.body, st, self.cmdline, 'footer')

        self.alarm_handle = main.set_alarm_in(1.5, self.remove_splash)
        self.seen_escape = False

        super().__init__(top)
        self.open_pop_up()
        return


    def get_pop_up_parameters(self):
        cols, rows = self.main.screen.get_cols_rows()

        L = int((cols - self.splash_width) / 2)
        T = int((rows - self.splash_height) / 2)
        
        return {'left': L, 'top': T,
                'overlay_width': self.splash_width,
                'overlay_height': self.splash_height}

    def create_pop_up(self):
        sp = splash()

        self.splash_width = sp.splash_width
        self.splash_height = sp.splash_height

        urwid.connect_signal(sp, 'close',
                             lambda button: self.close_pop_up())
        return sp


# remove_splash()-- Remove the popup as a timed event.

    def remove_splash(self, main, data=None):
        self.close_pop_up()
        return


# Process a key in escape mode.

    def process_escape(self, size, key):
        if key == config.escape:
            super().keypress(size, key)

        else:
            cmd = config.esc_cmds.get(key, '')
            {
                }.get(cmd, self.nop)()
            pass

        return


# nop()-- No-operation for undefined keys.

    def nop(self):
        return



# keypress()-- Intercept keys.

    def keypress(self, size, key):
        if self.seen_escape:
            self.process_escape(size, key)
            self.seen_escape = False

        elif key == config.escape:
            self.seen_escape = True

        else:
            return super().keypress(size, key)
            
        self.status.set_esc_status(self.seen_escape)
        return None

    pass


main = urwid.MainLoop(None, palette=config.palette, pop_ups=True)
main.widget = top_frame(main)

main.run()

