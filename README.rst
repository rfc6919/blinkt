******
blinkt
******

How I drive a `blinkt <https://shop.pimoroni.com/products/blinkt>`_.

- ``apa102.py`` - bitbang SPI for APA102 LEDs. works as a context
  handler for nice cleanup, and uses gpiod instead of pi-specific GPIO.
- ``cpuusage.py`` - a generator for cpu usage stats, read from
  ``/proc/stat``.
- ``blinkt-cpu.py`` - shows a colour cycle, faster as cpu idle time
  decreases.
