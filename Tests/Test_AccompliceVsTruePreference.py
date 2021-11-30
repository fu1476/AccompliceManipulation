# Find instances such that no-regret accomplice manipulation beats GS

from AccompliceManipulation import *
from GenerateRandomMarriageInstance import *

# INITIALIZE VARIABLES BEFORE RUNNING
iterations = 1000
min_n = 5
max_n = 10

manipulator = 1

for n in range(min_n, max_n + 1):
    for i in range(iterations):
        preferences = generate_uniform(n)
        mpref = preferences[0]
        wpref = preferences[1]

        gs_matches = gale_shapley(mpref, wpref)
        gs_partner = gs_matches.index(manipulator) + 1
        rank_of_gs_partner = wpref[manipulator - 1].index(gs_partner) + 1

        for accomplice in range(1, n + 1):
            results = accomplice_manipulation(mpref, wpref, manipulator, accomplice)
            partner = results[0].index(manipulator) + 1
            rank_of_partner = wpref[manipulator - 1].index(partner) + 1
            if rank_of_partner < rank_of_gs_partner:
                print("mpref =", mpref)
                print("wpref =", wpref)
                print("accomplice =", accomplice)
                print("manipulated results =", results[0])
                print("manipulated list =", results[1])
                print()
