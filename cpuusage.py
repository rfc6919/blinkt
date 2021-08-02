#!/usr/bin/python3

import collections

CpuUsagePercentages = collections.namedtuple('CpuUsagePercentages',
    'user nice system idle iowait irq softirq steal guest guest_nice')

class CpuUsage:
    def __init__(self):
        self._previous = None
        self.percentages = None
        self._get_next()

    def __iter__(self):
        return self

    def __next__(self):
        self._get_next()
        return self.percentages

    def _get_next(self):
        with open('/proc/stat') as procstat:
            line = procstat.readline()
        elements_text = line.split()
        if elements_text[0] != 'cpu':
            raise(RuntimeError(f'bad line from /proc/stat: {line}'))
        elements = [int(x) for x in elements_text[1:]]
        if self._previous is None:
            self._previous = [0] * len(elements)
        if len(elements) != len(self._previous):
            raise(RuntimeError(f'len(elements) changed'))
        diffs = [this-prev for this, prev in zip(elements, self._previous)]
        total = sum(diffs)
        if total > 0:
            self.percentages = CpuUsagePercentages(*[round(100*diff/total) for diff in diffs])
        self._previous = elements


if __name__ == '__main__':
    import time

    for percentages in CpuUsage():
        print(percentages)
        time.sleep(1)
