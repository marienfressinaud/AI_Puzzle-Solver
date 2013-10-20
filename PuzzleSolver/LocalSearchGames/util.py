# -*- coding: utf-8 -*-

from time import time


def perf(f, *args):
    start = time()
    res = apply(f, list(args))
    print "Elapsed time: %2f seconds" % (time() - start)
    return res
