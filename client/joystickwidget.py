#!/usr/bin/python
import math
import tkinter as tk

from vars import color_can

#TODO: detect angle of rotation for wheels
#TODO: detect speed
#TODO: declare events for external app

class JoystickWidget(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, parent)

        w = 200     # widget width
        h = 200     # widget height
        self.radius = 90
        self.jstkRadius = 10
        self.cx = w/2   # center x
        self.cy = h/2   # center y

        self.can_jsk = tk.Canvas(self, bg=color_can, height=h, width=w, highlightthickness=0)  # define a canvas
        self.can_jsk.pack()
        self.can_jsk.create_oval(self.cx-self.radius, self.cy-self.radius,
                                 self.cx+self.radius, self.cy+self.radius,
                                 fill='lightgrey', outline='white')

        self.jstkPtr = self.can_jsk.create_oval(self.cx - self.jstkRadius, self.cy - self.jstkRadius,
                                                self.cx + self.jstkRadius, self.cy + self.jstkRadius,
                                                fill='darkgrey', outline='white')

        self.can_jsk.bind('<Button-1>', self.LButtonClick)
        self.can_jsk.bind('<ButtonRelease-1>', self.LButtonRelease)
        self.can_jsk.bind('<B1-Motion>', self.MouseMove)

    def placeJskPtr(self, x, y):
        dst = self.distance(self.cx, self.cy, x, y)
        if dst > (self.radius-self.jstkRadius):
            c_adj = (self.radius-self.jstkRadius)/dst
            x = self.cx + (x-self.cx)*c_adj
            y = self.cy + (y-self.cy)*c_adj

        self.can_jsk.coords(self.jstkPtr,
                            x-self.jstkRadius, y-self.jstkRadius,
                            x+self.jstkRadius, y+self.jstkRadius)

    def LButtonClick(self, event):
        print('Left Button click')

    def LButtonRelease(self, event):
        print('Left Button Release')
        self.can_jsk.coords(self.jstkPtr,
                            self.cx-self.jstkRadius, self.cy-self.jstkRadius,
                            self.cx+self.jstkRadius, self.cy+self.jstkRadius)

    def MouseMove(self, event):
        print('MouseMove x %s; y %s distance %s' % (event.x, event.y, self.distance(self.cx, self.cy, event.x, event.y)))
        self.placeJskPtr(event.x, event.y)


    def distance(self, x1, y1, x2, y2):
        return math.sqrt(math.pow(x2-x1, 2)+math.pow(y2-y1, 2))

    def get(self):
        return self.entry.get()