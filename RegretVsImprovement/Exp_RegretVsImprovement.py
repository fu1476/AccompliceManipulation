from GaleShapley import *
from GenerateRandomMarriageInstance import *
from xlwt import Workbook

# INITIALIZE VARIABLES BEFORE RUNNING
iterations = 1000
min_n = 3
max_n = 40

manipulator = 1
accomplice = 1

wb = Workbook()
sheet_improvement_max_for_w = wb.add_sheet("Improvement (max for w)")
sheet_regret_max_for_w = wb.add_sheet("Regret (max for w)")
sheet_improvement_min_for_m = wb.add_sheet("Improvement (min for m)")
sheet_regret_min_for_m = wb.add_sheet("Regret (min for m)")
col_count = 0

for n in range(min_n, max_n + 1):
    sheet_improvement_max_for_w.write(0, col_count, "n=" + str(n))
    sheet_regret_max_for_w.write(0, col_count, "n=" + str(n))
    sheet_improvement_min_for_m.write(0, col_count, "n=" + str(n))
    sheet_regret_min_for_m.write(0, col_count, "n=" + str(n))
    xls_count = 0

    for i in range(iterations):
        mpref, wpref = generate_uniform(n)
        gs_matches = gale_shapley(mpref, wpref)
        rank_of_gs_partner_of_manipulator = get_w_rank(manipulator, wpref, gs_matches)
        rank_of_gs_partner_of_accomplice = get_m_rank(accomplice, mpref, gs_matches)
        mpref_new = mpref[:]

        all_beneficial_strategies = []
        for w in range(rank_of_gs_partner_of_accomplice, n):
            temp = mpref[accomplice - 1][:]
            woman = temp[w]
            temp.remove(woman)
            temp.insert(0, woman)
            mpref_new[accomplice - 1] = temp
            matches_new = gale_shapley(mpref_new, wpref)

            rank_of_manipulated_partner_of_accomplice = get_m_rank(accomplice, mpref, matches_new)
            rank_difference_for_accomplice = rank_of_gs_partner_of_accomplice - rank_of_manipulated_partner_of_accomplice
            rank_of_manipulated_partner_of_manipulator = get_w_rank(manipulator, wpref, matches_new)
            rank_difference_for_manipulator = rank_of_gs_partner_of_manipulator - rank_of_manipulated_partner_of_manipulator

            if rank_difference_for_manipulator > 0:
                strategy = (rank_difference_for_manipulator, rank_difference_for_accomplice)
                all_beneficial_strategies.append(strategy)

        strategy_max_for_w = (0, -n)
        strategy_min_for_m = (0, -n)
        for strategy in all_beneficial_strategies:
            if strategy[1] > strategy_min_for_m[1]:
                strategy_min_for_m = strategy
            if strategy[0] > strategy_max_for_w[0] or (strategy[0] == strategy_max_for_w[0] and strategy[1] > strategy_min_for_m[1]):
                strategy_max_for_w = strategy

        if strategy_max_for_w[0] > 0:
            xls_count += 1
            sheet_improvement_max_for_w.write(xls_count, col_count, strategy_max_for_w[0])
            sheet_regret_max_for_w.write(xls_count, col_count, strategy_max_for_w[1])
            sheet_improvement_min_for_m.write(xls_count, col_count, strategy_min_for_m[0])
            sheet_regret_min_for_m.write(xls_count, col_count, strategy_min_for_m[1])

        print("n =", n, "  i =", i)

    col_count += 1
    wb.save("RegretVsImprovement_n=" + str(max_n) + ".xls")
