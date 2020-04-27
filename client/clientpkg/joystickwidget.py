#!/usr/bin/python
import math
import tkinter as tk

from clientpkg.vars import color_can
from clientpkg.eventhook import EventHook

import enum


# Using enum class create enumerations
class EventTypes(enum.Enum):
    Finish = 1
    Motion = 2


class JoystickEvent(object):
    def __init__(self, type):
        self.type = type

    @classmethod
    def motionevent(cls, speed, angle):
        cls.speed = speed
        cls.angle = angle
        return cls(EventTypes.Motion)


def distance(x1, y1, x2, y2):
    dst = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
    angle = math.degrees(math.acos((x2 - x1) / dst))
    return dst, angle


def speed(y1, y2, max_y):
    dst = y1 - y2
    if dst > max_y:
        dst = max_y
    return dst / max_y


class JoystickWidget(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        tk.Frame.__init__(self, parent)

        # events
        self.OnThrottleFwd = EventHook()
        self.OnThrottleBack = EventHook()
        self.OnThrottleStop = EventHook()
        self.OnSteeringLeft = EventHook()
        self.OnSteeringRight = EventHook()
        self.OnSteeringCenter = EventHook()

        w = 200  # widget width
        h = 200  # widget height
        self.radius = 90
        self.jstkRadius = 10
        self.cx = w / 2  # center x
        self.cy = h / 2  # center y

        self.can_jsk = tk.Canvas(self, bg=color_can, height=h, width=w, highlightthickness=0)  # define a canvas
        self.can_jsk.pack()
        self.can_jsk.create_oval(self.cx - self.radius, self.cy - self.radius,
                                 self.cx + self.radius, self.cy + self.radius,
                                 fill='lightgrey', outline='white')

        self.arc_f = self.can_jsk.create_arc(self.cx - self.radius, self.cy - self.radius,
                                             self.cx + self.radius, self.cy + self.radius,
                                             style='chord', start=270, extent=0, fill='darkgreen')

        self.arc_r = self.can_jsk.create_arc(self.cx - self.radius, self.cy - self.radius,
                                             self.cx + self.radius, self.cy + self.radius,
                                             start=0, extent=0, fill='orange')

        self.arc_l = self.can_jsk.create_arc(self.cx - self.radius, self.cy - self.radius,
                                             self.cx + self.radius, self.cy + self.radius,
                                             start=180, extent=0, fill='orange')

        self.can_jsk.create_line(self.cx, self.cy - self.radius, self.cx, self.cy + self.radius,
                                 fill='darkgrey')
        self.can_jsk.create_line(self.cx - self.radius, self.cy, self.cx + self.radius, self.cy,
                                 fill='darkgrey')

        self.jstkPtr = self.can_jsk.create_oval(self.cx - self.jstkRadius, self.cy - self.jstkRadius,
                                                self.cx + self.jstkRadius, self.cy + self.jstkRadius,
                                                fill='navy', outline='white')

        self.can_jsk.bind('<Button-1>', self.LButtonClick)
        self.can_jsk.bind('<ButtonRelease-1>', self.LButtonRelease)
        self.can_jsk.bind('<B1-Motion>', self.MouseMove)

    def placeJskPtr(self, x, y):
        dst, angle = distance(self.cx, self.cy, x, y)
        spd = speed(self.cy, y, self.radius) * 90
        if dst > (self.radius - self.jstkRadius):
            c_adj = (self.radius - self.jstkRadius) / dst
            x = self.cx + (x - self.cx) * c_adj
            y = self.cy + (y - self.cy) * c_adj

        self.can_jsk.coords(self.jstkPtr,
                            x - self.jstkRadius, y - self.jstkRadius,
                            x + self.jstkRadius, y + self.jstkRadius)

        self.can_jsk.itemconfigure(self.arc_r, start=0, extent=angle - 90)
        self.can_jsk.itemconfigure(self.arc_l, start=180, extent=angle - 90)
        self.can_jsk.itemconfigure(self.arc_f, start=270 - spd, extent=spd * 2)

    def LButtonClick(self, event):
        print('Left Button click')

    def LButtonRelease(self, event):
        print('Left Button Release')
        self.can_jsk.coords(self.jstkPtr,
                            self.cx - self.jstkRadius, self.cy - self.jstkRadius,
                            self.cx + self.jstkRadius, self.cy + self.jstkRadius)
        self.can_jsk.itemconfigure(self.arc_r, start=0, extent=0)
        self.can_jsk.itemconfigure(self.arc_l, start=180, extent=0)
        self.can_jsk.itemconfigure(self.arc_f, start=270, extent=0)
        self.fireEvents(JoystickEvent(EventTypes.Finish))

    def MouseMove(self, event):
        dst, angle = distance(self.cx, self.cy, event.x, event.y)
        spd = speed(self.cy, event.y, self.radius)
        print('MouseMove x %s; y %s distance %s; angle %s; speed %s' % (event.x, event.y, dst, angle, spd))
        self.placeJskPtr(event.x, event.y)
        self.fireEvents(JoystickEvent.motionevent(spd, angle))

    def get(self):
        return self.entry.get()

    def fireEvents(self, event):
        if event.type == EventTypes.Finish:
            self.OnThrottleStop.fire()
            self.OnSteeringCenter.fire()
        elif event.type == EventTypes.Motion:
            if event.speed > 0:
                self.OnThrottleFwd.fire()
            if event.angle > 90:
                self.OnSteeringLeft.fire()
            else:
                self.OnSteeringLeft.fire()
