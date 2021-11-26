import time
import os
import sys
import psutil
import blinkt
from subprocess import PIPE, Popen
import threading

def _get_cpu_temperature():
    process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
    output, _error = process.communicate()
    output = output.decode()

    pos_start = output.index('=') + 1
    pos_end = output.rindex("'")

    temp = float(output[pos_start:pos_end])

    return temp

def _show_graph(v, r=255, g=255, b=255):
    v *= blinkt.NUM_PIXELS
    for x in range(blinkt.NUM_PIXELS):
        if v < 0:
            r, g, b = 0, 0, 0
        else:
            r, g, b = [int(min(v, 1.0) * c) for c in [r, g, b]]
        blinkt.set_pixel(x, r, g, b)
        v -= 1

def get_cpu_load():
    v = psutil.cpu_percent() / 100.0
    _show_graph(v, r=0, g=0)

def get_cpu_temp():
    v = _get_cpu_temperature() / 70.0
    _show_graph(v, g=0, b=0)

class Blinker:

    def __init__(self, brightness=0.1, *args) -> None:
        self.views = {"default": [*args]}
        blinkt.set_brightness(min(brightness, 1))
        blinkt.set_clear_on_exit()
        self.mode = "default"

    def set_view_mode(self, mode: str):
        self.mode = mode

    def add_views(self, mode_name, *views):
        self.views[mode_name] = [*views]

    def show(self):
        blink_thread = threading.Thread(target=self._show, daemon=True) # Make sure we don't wait indefinitely after script ends
        blink_thread.start()
        
    def _show(self): 
        while True:
            for view in self.views[self.mode]:
                view()
                blinkt.show()
                time.sleep(2)


if __name__ == '__main__':
    blinker = Blinker(float(sys.argv[1]), get_cpu_load, get_cpu_temp)
    blinker.show()
    while True:
        print("I'm doing stuff while it blinks!")
        time.sleep(1)