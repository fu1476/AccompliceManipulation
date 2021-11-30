from SelfManipulation import *
from AccompliceManipulation import *
from GenerateRandomMarriageInstance import *
from xlwt import Workbook

# INITIALIZE VARIABLES BEFORE RUNNING
iterations = 1000
n_values = [10, 20, 30, 40]

manipulator = 1

wb = Workbook()
for n in n_values:
    sheet = wb.add_sheet("n=" + str(n))
    sheet.write(0, 0, "# of potential accomplices")
    sheet.write(0, 1, "SvTP")
    sheet.write(0, 2, "NRvTP")
    sheet.write(0, 3, "WRvTP")
    sheet.write(0, 4, "SvNR")
    sheet.write(0, 5, "SvWR")
    sheet.write(0, 6, "NRvS")
    sheet.write(0, 7, "WRvS")

    self_beats_gs = 0
    nr_beats_gs_list = [0 for i in range(n)]
    wr_beats_gs_list = [0 for i in range(n)]
    self_beats_nr_list = [0 for i in range(n)]
    self_beats_wr_list = [0 for i in range(n)]
    nr_beats_self_list = [0 for i in range(n)]
    wr_beats_self_list = [0 for i in range(n)]
    total_successful_nr_accomplices = 0
    total_successful_wr_accomplices = 0

    for i in range(iterations):
        mpref, wpref = generate_uniform(n)
        gs_matches = gale_shapley(mpref, wpref)
        rank_of_gs_partner = get_w_rank(manipulator, wpref, gs_matches)

        self_results = self_manipulation(mpref, wpref, manipulator)
        rank_of_self_partner = get_w_rank(manipulator, wpref, self_results[0])
        if rank_of_self_partner < rank_of_gs_partner:
            self_beats_gs += 1 /iterations

        all_nr_ranks = []
        all_wr_ranks = []
        for accomplice in range(1, n + 1):
            nr_results = accomplice_manipulation(mpref, wpref, manipulator, accomplice)
            rank_of_nr_partner = get_w_rank(manipulator, wpref, nr_results[0])
            all_nr_ranks.append(rank_of_nr_partner)
            if rank_of_nr_partner < rank_of_gs_partner:
                total_successful_nr_accomplices += 1

            wr_results = accomplice_manipulation(mpref, wpref, manipulator, accomplice, with_regret=True)
            rank_of_wr_partner = get_w_rank(manipulator, wpref, wr_results[0])
            all_wr_ranks.append(rank_of_wr_partner)
            if rank_of_wr_partner < rank_of_gs_partner:
                total_successful_wr_accomplices += 1

        for x in range(1, n + 1):
            min_nr_rank = min(all_nr_ranks)
            if min_nr_rank < rank_of_gs_partner:
                nr_beats_gs_list[n - x] += 1 / iterations
            if rank_of_self_partner < min_nr_rank:
                self_beats_nr_list[n - x] += 1 / iterations
            if min_nr_rank < rank_of_self_partner:
                nr_beats_self_list[n - x] += 1 / iterations
            if x != n:
                all_nr_ranks = all_nr_ranks[:-1]

            min_wr_rank = min(all_wr_ranks)
            if min_wr_rank < rank_of_gs_partner:
                wr_beats_gs_list[n - x] += 1 / iterations
            if rank_of_self_partner < min_wr_rank:
                self_beats_wr_list[n - x] += 1 / iterations
            if min_wr_rank < rank_of_self_partner:
                wr_beats_self_list[n - x] += 1 / iterations
            if x != n:
                all_wr_ranks = all_wr_ranks[:-1]

        print("n =", n, "i =", i)

    for x in range(n):
        write = sheet.write(x + 1, 0, x + 1)
        sheet.write(x + 1, 1, self_beats_gs)
        sheet.write(x + 1, 2, nr_beats_gs_list[x])
        sheet.write(x + 1, 3, wr_beats_gs_list[x])
        sheet.write(x + 1, 4, self_beats_nr_list[x])
        sheet.write(x + 1, 5, self_beats_wr_list[x])
        sheet.write(x + 1, 6, nr_beats_self_list[x])
        sheet.write(x + 1, 7, wr_beats_self_list[x])

    wb.save("VaryingAccomplicePools_n=" + str(max(n_values)) + ".xls")
