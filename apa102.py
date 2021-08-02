import gpiod

class APA102:
    def __init__(self, pixel_count=8, gpio_chip="gpiochip0", gpio_clk=24, gpio_dat=23, consumer_name="apa102", clear_on_enter=True,  clear_on_exit=True):
        self.pixel_count = pixel_count
        self.consumer_name = consumer_name
        self.clear_on_enter = clear_on_enter
        self.clear_on_exit = clear_on_exit

        self.chip = gpiod.Chip(gpio_chip)
        self.lines = self.chip.get_lines([gpio_clk, gpio_dat])

    def __del__(self):
        self.chip.close()

    def _request(self):
        self.lines.request(consumer=self.consumer_name, type=gpiod.LINE_REQ_DIR_OUT)

    def _release(self):
        self.lines.release()

    def _clear(self):
        self.send([[0,0,0,0]]*self.pixel_count)

    def __enter__(self):
        self._request()
        if self.clear_on_enter:
            self._clear()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.clear_on_exit:
            self._clear()
        self._release()

    def _tx_octet(self, octet):
        for bit in range(8):
            dat = octet & (0x80 >> bit)
            self.lines.set_values([1, dat])
            self.lines.set_values([0, dat])

    def send(self, buffer):

        for header in range(4):
            self._tx_octet(0x00)

        for pixel in buffer:
            r, g, b, brightness = pixel
            self._tx_octet(brightness | 0b11100000)
            self._tx_octet(b)
            self._tx_octet(g)
            self._tx_octet(r)

        for trailer in range(4):
            self._tx_octet(0xff)
