# Tests whether simultaneous improvement for a man and woman who manipulate together is ever possible
# Note: Demange, Gale, Sotomayor (1987) proved that this is impossible

from GaleShapley import *
from GenerateRandomMarriageInstance import *
import itertools

# INITIALIZE VARIABLES BEFORE RUNNING
iterations = 100
min_n = 3
max_n = 6

for n in range(min_n, max_n + 1):
    for i in range(iterations):
        preferences = generate_uniform(n)
        mpref = preferences[0]
        wpref = preferences[1]

        gs_matches = gale_shapley(mpref, wpref)

        # manipulator = woman; accomplice = man
        for manipulator in range(1, n + 1):
            gs_partner_of_manip = gs_matches.index(manipulator) + 1
            rank_of_gs_partner_of_manip = wpref[manipulator - 1].index(gs_partner_of_manip) + 1

            for accomplice in range(1, n + 1):
                gs_partner_of_acc = gs_matches[accomplice - 1]
                rank_of_gs_partner_of_acc = mpref[accomplice - 1].index(gs_partner_of_acc) + 1

                wpref_new = wpref[:]
                mpref_new = mpref[:]

                all_permutations_manip = list(itertools.permutations(range(1, n + 1)))
                for perm_manip in all_permutations_manip:
                    wpref_new[manipulator - 1] = list(perm_manip)

                    all_permutations_acc = list(itertools.permutations(range(1, n + 1)))
                    for perm_acc in all_permutations_acc:
                        mpref_new[accomplice - 1] = list(perm_acc)

                        matches_new = gale_shapley(mpref_new, wpref_new)
                        simul_manip_partner_of_manip = matches_new.index(manipulator) + 1
                        rank_of_simul_manip_partner_of_manip = wpref[manipulator - 1].index(simul_manip_partner_of_manip) + 1
                        simul_manip_partner_of_acc = matches_new[accomplice - 1]
                        rank_of_simul_manip_partner_of_acc = mpref[accomplice - 1].index(simul_manip_partner_of_acc) + 1

                        if rank_of_simul_manip_partner_of_manip <= rank_of_gs_partner_of_manip:
                            if rank_of_simul_manip_partner_of_acc < rank_of_gs_partner_of_acc:
                                print("mpref =", mpref)
                                print("wpref =", wpref)
                                print("manipulator =", manipulator)
                                print("accomplice =", accomplice)
                                print("single man manipulated list =", mpref_new[accomplice - 1])
                                print("single woman manipulated list =", wpref_new[manipulator - 1])
                                print("gale-shapley results =", gs_matches)
                                print("manipulated results =", matches_new)
                                print(gs_partner_of_acc, simul_manip_partner_of_acc)
                                print(gs_partner_of_manip, simul_manip_partner_of_manip)
                                print()

        print("n =", n, "and i =", i)
