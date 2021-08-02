#!/usr/bin/python3

import colorsys
import time
import apa102
import cpuusage

brightness = 1
#brightness = 8
#brightness = 16
spacing = 360.0 / 8
sleep_time = 0.05
theta = 360 * sleep_time / 300 # 300s to complete a cycle

n = 0

with apa102.APA102() as blinkt:
    for percentages in cpuusage.CpuUsage():
        for i in range(5):
            n += 10 * (100-percentages.idle)
            buffer = []
            for x in range(8):
                h = ( ( n*theta + x*spacing ) % 360.0 ) / 360.0
                r, g, b = [int(c * 32) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
                pixel = [r, g, b, brightness]
                buffer.append(pixel)
            blinkt.send(buffer)
            time.sleep(sleep_time)
