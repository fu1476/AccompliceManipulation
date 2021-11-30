from GaleShapley import *


def accomplice_manipulation(mpref, wpref, manipulator, accomplice, with_regret=False):
    n = len(mpref)

    if accomplice == -1:
        return test_all_accomplices(mpref, wpref, manipulator, n)

    gs_matches = gale_shapley(mpref, wpref)
    manipulated_matches = gs_matches[:]
    manipulated_list = mpref[accomplice - 1][:]
    mpref_new = mpref[:]

    rank_of_gs_partner_of_manipulator = get_w_rank(manipulator, wpref, gs_matches)
    rank_of_gs_partner_of_accomplice = get_m_rank(accomplice, mpref, gs_matches)

    best_rank_of_partner = n + 1
    for i in range(rank_of_gs_partner_of_accomplice, n):
        temp = mpref[accomplice - 1][:]
        woman = temp[i]

        if with_regret or wpref[woman - 1].index(accomplice) < get_w_rank(woman, wpref, gs_matches):
            temp.remove(woman)
            temp.insert(0, woman)
            mpref_new[accomplice - 1] = temp
            matches_new = gale_shapley(mpref_new, wpref)

            rank_of_manipulated_partner_of_accomplice = get_m_rank(accomplice, mpref, matches_new)
            if with_regret or rank_of_manipulated_partner_of_accomplice == rank_of_gs_partner_of_accomplice:
                rank_of_manipulated_partner_of_manipulator = get_w_rank(manipulator, wpref, matches_new)
                if rank_of_manipulated_partner_of_manipulator < best_rank_of_partner:
                    best_rank_of_partner = rank_of_manipulated_partner_of_manipulator
                    if rank_of_manipulated_partner_of_manipulator < rank_of_gs_partner_of_manipulator:
                        manipulated_list = temp[:]
                        manipulated_matches = matches_new[:]

    return manipulated_matches, manipulated_list


def test_all_accomplices(mpref, wpref, manipulator, n):
    best_rank_of_partner = n + 1
    best_accomplice = 0
    best_matches = 0
    best_list = []
    for accomplice in range(1, n + 1):
        results = accomplice_manipulation(mpref, wpref, manipulator, accomplice)
        rank_of_partner = get_w_rank(manipulator, wpref, results[0])
        if rank_of_partner < best_rank_of_partner:
            best_rank_of_partner = rank_of_partner
            best_accomplice = accomplice
            best_matches = results[0]
            best_list = results[1]

    return best_matches, best_list, best_accomplice
