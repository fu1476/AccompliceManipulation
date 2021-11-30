def gale_shapley(mpref, wpref, strategic_woman=0):
    n = len(mpref)
    curr_match_count = 0
    last_rejected_by_rank_what = [0 for i in range(n)]
    men_matchings = [0 for i in range(n)]
    women_matchings = [0 for i in range(n)]
    proposals_to_strategic_woman = set()    # Only used if strategic_woman != 0

    # continue until all matches made
    while curr_match_count < n:
        for man in range(n):
            # if man is single
            if men_matchings[man] == 0:
                # get first non-rejecting woman from man's preference list
                woman = mpref[man][last_rejected_by_rank_what[man]] - 1
                if woman + 1 == strategic_woman:
                    proposals_to_strategic_woman.add(man + 1)

                # both man and woman are single
                if women_matchings[woman] == 0:
                    # create match (man, woman)
                    men_matchings[man] = woman + 1
                    women_matchings[woman] = man + 1
                    curr_match_count += 1

                # woman is with someone
                else:
                    # find ranks of curr_partner and man given woman's preference list
                    curr_partner = women_matchings[woman]
                    curr_partner_rank = wpref[woman].index(curr_partner)
                    man_rank = wpref[woman].index(man + 1)

                    # woman prefers curr_partner over man
                    if curr_partner_rank < man_rank:
                        last_rejected_by_rank_what[man] = mpref[man].index(woman + 1) + 1

                    # woman prefers man over curr_partner
                    else:
                        men_matchings[curr_partner - 1] = 0
                        last_rejected_by_rank_what[curr_partner - 1] = mpref[curr_partner - 1].index(woman + 1) + 1
                        men_matchings[man] = woman + 1
                        women_matchings[woman] = man + 1

    if strategic_woman != 0:
        return men_matchings, proposals_to_strategic_woman
    else:
        return men_matchings


def get_m_partner(m, matches):
    return matches[m - 1]


def get_w_partner(w, matches):
    return matches.index(w) + 1


def get_m_rank(m, mpref, matches):
    partner = matches[m - 1]
    return mpref[m - 1].index(partner) + 1


def get_w_rank(w, wpref, matches):
    partner = matches.index(w) + 1
    return wpref[w - 1].index(partner) + 1


# Checks if matching1 Pareto-improves matching2 for the set of all women
def pareto_improvement_women(wpref, matching1, matching2):
    n = len(matching1)
    matching1_ranks = [get_w_rank(w, wpref, matching1) for w in range(1, n + 1)]
    matching2_ranks = [get_w_rank(w, wpref, matching2) for w in range(1, n + 1)]
    ranks_difference = [matching2_ranks[i] - matching1_ranks[i] for i in range(n)]
    improvement = False
    for diff in ranks_difference:
        if diff < 0:
            return False
        if diff > 0:
            improvement = True
    return improvement


def check_stability(mpref, wpref, matching, return_blocking_pairs=False):
    n = len(mpref)
    blocking_pairs = []

    for m in range(1, n + 1):
        m_partner = matching[m - 1]
        rank_of_m_partner = mpref[m - 1].index(m_partner) + 1
        for w in range(1, n + 1):
            w_partner = matching.index(w) + 1
            rank_of_w_partner = wpref[w - 1].index(w_partner) + 1

            # if (m, w) is not a matching
            if matching[m - 1] != w:
                rank_of_w_for_m = mpref[m - 1].index(w) + 1
                rank_of_m_for_w = wpref[w - 1].index(m) + 1
                if rank_of_m_partner > rank_of_w_for_m and rank_of_w_partner > rank_of_m_for_w:
                    if return_blocking_pairs:
                        bp = (m, w)
                        blocking_pairs.append(bp)
                    else:
                        return False

    if return_blocking_pairs:
        return blocking_pairs
    else:
        return True


if __name__ == "__main__":
    mpref = [[5, 2, 1, 4, 3, 6], [1, 5, 6, 3, 2, 4], [2, 4, 3, 1, 6, 5], [5, 2, 6, 3, 1, 4], [6, 3, 1, 4, 5, 2], [3, 2, 4, 1, 5, 6]]
    wpref = [[1, 6, 3, 4, 5, 2], [6, 4, 5, 1, 2, 3], [4, 5, 3, 1, 2, 6], [6, 5, 4, 3, 1, 2], [3, 5, 2, 4, 1, 6], [5, 6, 1, 3, 2, 4]]
    print(gale_shapley(mpref, wpref))
