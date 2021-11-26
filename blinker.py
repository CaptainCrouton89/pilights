import time
import sys
import blinkt
import threading
from pilights import blinkFunctions, templates


class Blinker:

    def __init__(self, brightness: float=0.1, *args) -> None:
        self.views = {"default": list(*args)}
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
    blinker = Blinker(float(sys.argv[1]), templates.DEFAULT)
    blinker.show()
    while True:
        print("I'm doing stuff while it blinks!")
        time.sleep(1)