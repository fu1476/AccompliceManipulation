from GaleShapley import *


def self_manipulation(mpref, wpref, manipulator, return_all_strategies=False):
    n = len(mpref)

    # initial run of gale_shapley
    gs_matching, all_proposers = gale_shapley(mpref, wpref, manipulator)
    exhausted_proposers = [get_w_partner(manipulator, gs_matching)]

    proposer_dict = {}  # key = proposer; value = manipulated  preference list
    strategy = (gs_matching, wpref[manipulator - 1][:])
    all_strategies = [strategy]

    # update proposer_dict to include all proposers from the initial run
    for proposer in all_proposers:
        proposer_dict.update({proposer: wpref[manipulator - 1][:]})

    # loop until all potential proposers are exhausted
    while len(exhausted_proposers) != len(all_proposers):
        all_proposers_copy = all_proposers.copy()

        # for all proposers that haven't been exhausted
        for proposer in all_proposers:
            if proposer not in exhausted_proposers:
                # create a new manipulated list with proposer in front
                new_list = proposer_dict[proposer]
                new_list.remove(proposer)
                new_list.insert(0, proposer)
                exhausted_proposers.append(proposer)

                # update each non-exhausted proposer's list in proposer_dict
                for prop in proposer_dict:
                    if prop not in exhausted_proposers:
                        proposer_dict.update({proposer: new_list[:]})

                # run gale_shapley using the new manipulated list
                wpref_new = wpref[:]
                wpref_new[manipulator - 1] = new_list
                new_matching, new_proposers = gale_shapley(mpref, wpref_new, manipulator)
                all_proposers_copy = all_proposers_copy.union(new_proposers)
                strategy = (new_matching[:], new_list[:])
                all_strategies.append(strategy)

                # update proposer_dict to include any new proposers
                for prop in all_proposers_copy:
                    if prop not in exhausted_proposers and prop not in proposer_dict:
                        proposer_dict.update({prop: wpref_new[manipulator - 1][:]})

        # update all_proposers
        all_proposers = all_proposers_copy

    if return_all_strategies:
        return all_strategies

    # find cheater's best ranking man from all those who proposed
    best_man_rank = n + 1
    best_strategy = None
    for strategy in all_strategies:
        rank = get_w_rank(manipulator, wpref, strategy[0])
        if rank < best_man_rank:
            best_man_rank = rank
            best_strategy = strategy

    return best_strategy
