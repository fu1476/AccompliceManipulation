# Find with-regret accomplice manipulation instances such that:
# 1) WR > NR > GS
# 2) More than 2 women are strictly worse off

from AccompliceManipulation import *
from GenerateRandomMarriageInstance import *

# INITIALIZE VARIABLES BEFORE RUNNING
iterations = 100000
min_n = 5
max_n = 5

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
            rank_of_partner = get_w_rank(manipulator, wpref, results[0])

            regret_results = accomplice_manipulation(mpref, wpref, manipulator, accomplice, with_regret=True)
            rank_of_regret_partner = get_w_rank(manipulator, wpref, regret_results[0])

            if rank_of_gs_partner > rank_of_partner > rank_of_regret_partner:
                count = 0
                for w in range(1, n + 1):
                    gs_rank = get_w_rank(w, wpref, gs_matches)
                    manipulated_rank = get_w_rank(w, wpref, regret_results[0])
                    if gs_rank < manipulated_rank:
                        count += 1
                if count > 2:
                    print("mpref =", mpref)
                    print("wpref =", wpref)
                    print("GS matches =", gs_matches)
                    print("accomplice =", accomplice)
                    print("NR results =", results[0])
                    print("NR list =", results[1])
                    print("WR results =", regret_results[0])
                    print("WR list =", regret_results[1])
                    print()
