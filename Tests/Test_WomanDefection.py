from AccompliceManipulation import *
from SelfManipulation import *
from GenerateRandomMarriageInstance import *

# INITIALIZE VARIABLES BEFORE RUNNING
iterations = 10000
min_n = 10
max_n = 20

accomplice = 1
manipulator = 1

for n in range(min_n, max_n + 1):
    for i in range(iterations):
        mpref, wpref = generate_uniform(n)
        gs_matching = gale_shapley(mpref, wpref)
        gs_partner_of_accomplice_rank = get_m_rank(accomplice, mpref, gs_matching)

        accomplice_results = accomplice_manipulation(mpref, wpref, manipulator, accomplice)
        self_results = self_manipulation(mpref, wpref, manipulator)
        self_partner_of_manipulator_rank = get_w_rank(manipulator, wpref, self_results[0])

        defection_mpref = mpref[:]
        defection_mpref[accomplice - 1] = accomplice_results[1]
        self_defection_results = self_manipulation(defection_mpref, wpref, manipulator)
        self_defection_partner_of_accomplice_rank = get_m_rank(accomplice, mpref, self_defection_results[0])
        self_defection_partner_of_manipulator_rank = get_w_rank(manipulator, wpref, self_defection_results[0])

        if self_partner_of_manipulator_rank > self_defection_partner_of_manipulator_rank and gs_partner_of_accomplice_rank < self_defection_partner_of_accomplice_rank:
            print("mpref =", mpref)
            print("wpref =", wpref)
            print("Accomplice results:", accomplice_results)
            print("Defection results:", self_defection_results)
            print()
