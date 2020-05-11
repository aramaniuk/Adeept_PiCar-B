#!/usr/bin/python

import tkinter as tk

from clientpkg.vars import color_can

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

    def on_update_ultrasonic_data(self, ultrasonic_data):
        f_list = []
        dis_list = ultrasonic_data.split()  # Save the data as a list
        for i in range(0, len(dis_list)):  # Translate the String-type value in the list to Float-type
            try:
                new_f = float(dis_list[i])
                f_list.append(new_f)
            except:
                continue

        dis_list = f_list
        # can_scan.delete(line)
        # can_scan.delete(point_scan)
        can_scan_1 = tk.Canvas(root, bg=color_can, height=250, width=320,
                               highlightthickness=0)  # define a canvas
        can_scan_1.place(x=440, y=330)  # Place the canvas
        line = can_scan_1.create_line(0, 62, 320, 62, fill='darkgray')  # Draw a line on canvas
        line = can_scan_1.create_line(0, 124, 320, 124, fill='darkgray')  # Draw a line on canvas
        line = can_scan_1.create_line(0, 186, 320, 186, fill='darkgray')  # Draw a line on canvas
        line = can_scan_1.create_line(160, 0, 160, 250, fill='darkgray')  # Draw a line on canvas
        line = can_scan_1.create_line(80, 0, 80, 250, fill='darkgray')  # Draw a line on canvas
        line = can_scan_1.create_line(240, 0, 240, 250, fill='darkgray')  # Draw a line on canvas

        x_range = var_x_scan.get()  # Get the value of scan range from IntVar

        for i in range(0, len(dis_list)):  # Scale the result to the size as canvas
            try:
                len_dis_1 = int((dis_list[i] / x_range) * 250)  # 600 is the height of canvas
                pos = int((i / len(dis_list)) * 320)  # 740 is the width of canvas
                pos_ra = int(((i / len(dis_list)) * 140) + 20)  # Scale the direction range to (20-160)
                len_dis = int(
                    len_dis_1 * (math.sin(math.radians(pos_ra))))  # len_dis is the height of the line

                x0_l, y0_l, x1_l, y1_l = pos, (250 - len_dis), pos, (250 - len_dis)  # The position of line
                x0, y0, x1, y1 = (pos + 3), (250 - len_dis + 3), (pos - 3), (
                        250 - len_dis - 3)  # The position of arc

                if pos <= 160:  # Scale the whole picture to a shape of sector
                    pos = 160 - abs(int(len_dis_1 * (math.cos(math.radians(pos_ra)))))
                    x1_l = (x1_l - math.cos(math.radians(pos_ra)) * 130)
                else:
                    pos = abs(int(len_dis_1 * (math.cos(math.radians(pos_ra))))) + 160
                    x1_l = x1_l + abs(math.cos(math.radians(pos_ra)) * 130)

                y1_l = y1_l - abs(math.sin(math.radians(pos_ra)) * 130)  # Orientation of line

                line = can_scan_1.create_line(pos, y0_l, x1_l, y1_l,
                                              fill=color_line)  # Draw a line on canvas
                point_scan = can_scan_1.create_oval((pos + 3), y0, (pos - 3), y1, fill=color_oval,
                                                    outline=color_oval)  # Draw a arc on canvas
            except:
                pass
        can_tex_11 = can_scan_1.create_text((27, 178), text='%sm' % round((x_range / 4), 2),
                                            fill='#aeea00')  # Create a text on canvas
        can_tex_12 = can_scan_1.create_text((27, 116), text='%sm' % round((x_range / 2), 2),
                                            fill='#aeea00')  # Create a text on canvas
        can_tex_13 = can_scan_1.create_text((27, 54), text='%sm' % round((x_range * 0.75), 2),
                                            fill='#aeea00')  # Create a text on canvas