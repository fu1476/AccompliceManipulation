# Generates instances such that with-regret accomplice manipulation beats self manipulation

from SelfManipulation import *
from AccompliceManipulation import *
from GenerateRandomMarriageInstance import *

# INITIALIZE VARIABLES BEFORE RUNNING
iterations = 1000
min_n = 4
max_n = 4

manipulator = 1

self_beats_regret_acc = 0

for n in range(min_n, max_n + 1):
    for i in range(iterations):
        preferences = generate_uniform(n)
        mpref = preferences[0]
        wpref = preferences[1]

        self_results = self_manipulation(mpref, wpref, manipulator)
        self_partner = self_results[0].index(manipulator) + 1
        rank_of_self_partner = wpref[manipulator - 1].index(self_partner) + 1

        for accomplice in range(1, n + 1):
            regret_acc_results = accomplice_manipulation(mpref, wpref, manipulator, accomplice, with_regret=True)
            regret_acc_partner = regret_acc_results[0].index(manipulator) + 1
            rank_of_regret_acc_partner = wpref[manipulator - 1].index(regret_acc_partner) + 1
            if rank_of_regret_acc_partner > rank_of_self_partner:
                self_beats_regret_acc += 1
                print("mpref =", mpref)
                print("wpref =", wpref)
                print("self manipulated results =", self_results[0])
                print("with-regret accomplice manipulated results =", regret_acc_results[0])
                print("accomplice =", accomplice)
                print()

print("Total:", self_beats_regret_acc)
