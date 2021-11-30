import random
import math
import numpy as np


def generate_uniform(n):
    men_pref = []
    women_pref = []
    ordered = [i + 1 for i in range(n)]

    for i in range(n):
        mrand = ordered[:]
        random.shuffle(mrand)
        men_pref.append(mrand)

        wrand = ordered[:]
        random.shuffle(wrand)
        women_pref.append(wrand)

    return men_pref, women_pref
