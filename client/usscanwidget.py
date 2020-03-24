#!/usr/bin/python

import tkinter as tk

from vars import color_can

class USScanWidget(tk.Frame):
    def __init__(self, parent, x_range):
        self.parent = parent
        tk.Frame.__init__(self, parent)

        can_scan = tk.Canvas(self, bg=color_can, height=250, width=320, highlightthickness=0)  # define a canvas
        can_scan.pack()
        line = can_scan.create_line(0, 62, 320, 62, fill='darkgray')  # Draw a line on canvas
        line = can_scan.create_line(0, 124, 320, 124, fill='darkgray')  # Draw a line on canvas
        line = can_scan.create_line(0, 186, 320, 186, fill='darkgray')  # Draw a line on canvas
        line = can_scan.create_line(160, 0, 160, 250, fill='darkgray')  # Draw a line on canvas
        line = can_scan.create_line(80, 0, 80, 250, fill='darkgray')  # Draw a line on canvas
        line = can_scan.create_line(240, 0, 240, 250, fill='darkgray')  # Draw a line on canvas
        can_tex_11 = can_scan.create_text((27, 178), text='%sm' % round((x_range / 4), 2),
                                          fill='#aeea00')  # Create a text on canvas
        can_tex_12 = can_scan.create_text((27, 116), text='%sm' % round((x_range / 2), 2),
                                          fill='#aeea00')  # Create a text on canvas
        can_tex_13 = can_scan.create_text((27, 54), text='%sm' % round((x_range * 0.75), 2),
                                          fill='#aeea00')  # Create a text on canvas

    def get(self):
        return self.entry.get()