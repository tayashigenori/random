# -*- coding: utf-8 -*-

# https://github.com/nuodb/sysbench/blob/e38ffad3ec19da001350fbbff9d1fe44577dcf94/sysbench/sysbench.c

import random
import getopt, sys

"""
  --rand-init=[on|off]        initialize random number generator [off]
  --rand-type=STRING          random numbers distribution {uniform,gaussian,special,pareto} [special]
  --rand-spec-iter=N          number of iterations used for numbers generation [12]
  --rand-spec-pct=N           percentage of values to be treated as 'special' (for special distribution) [1]
  --rand-spec-res=N           percentage of 'special' values to use (for special distribution) [75]
  --rand-seed=N               seed for random number generator, ignored when 0 [0]
  --rand-pareto-h=N           parameter h for pareto distibution [0.2]
"""

try:
    opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "rand-spec-iter=", "rand-spec-pct=", "rand-spec-res="])
except getopt.GetoptError, err:
    # ヘルプメッセージを出力して終了
    print str(err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)
verbose = False
randSpecIter = 12
randSpecPct  = 1
randSpecRes  = 75
for o, a in opts:
    if o == "-v":
        verbose = True
    elif o in ("-h", "--help"):
        usage()
        sys.exit()
    elif o in ("-o", "--rand-spec-iter"):
        randSpecIter = int(a)
    elif o in ("-o", "--rand-spec-pct"):
        randSpecPct = int(a)
    elif o in ("-o", "--rand-spec-res"):
        randSpecRes = int(a)
    else:
        assert False, "unhandled option"

def sb_rand_special(a, b):
    sum = 0
    if a >= b:
        return 0

    t = b - a + 1
    #/* Increase range size for special values. */
    range_size = t * (100 / (100 - randSpecRes))

    #/* Generate uniformly distributed one at this stage  */
    #res = sb_rnd() % range_size;
    res = random.randrange(0, range_size)

    #/* For first part use gaussian distribution */
    if res < t:
      for i in range(0, randSpecIter):
        sum += random.randrange(0, t)
      return a + sum / randSpecIter

    #/*
    # * For second part use even distribution mapped to few items 
    # * We shall distribute other values near by the center
    # */
    d = t * randSpecPct / 100;
    if d < 1:
      d = 1
    res %= d

    #/* Now we have res values in SPECIAL_PCT range of the data */
    res += (t / 2 - t * randSpecPct / (100 * 2));

    return a + res

def main():
    for iter in range(100):
        print sb_rand_special(0, 80)


if __name__ == '__main__':
    main()

