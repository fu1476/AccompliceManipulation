from SelfManipulation import *
from AccompliceManipulation import *
from GenerateRandomMarriageInstance import *
from xlwt import Workbook

# INITIALIZE VARIABLES BEFORE RUNNING
iterations = 1000
min_n = 3
max_n = 40

manipulator = 1

wb = Workbook()
sheet_self = wb.add_sheet("Self")
sheet_acc = wb.add_sheet("Accomplice")
col_count = 0

for n in range(min_n, max_n + 1):
    sheet_acc.write(0, col_count, "n=" + str(n))
    sheet_self.write(0, col_count, "n=" + str(n))

    for i in range(iterations):
        mpref, wpref = generate_uniform(n)
        gs_matching = gale_shapley(mpref, wpref)
        rank_of_gs_partner = get_w_rank(manipulator, wpref, gs_matching)

        self_results = self_manipulation(mpref, wpref, manipulator)
        rank_of_self_partner = get_w_rank(manipulator, wpref, self_results[0])
        self_difference = rank_of_gs_partner - rank_of_self_partner
        sheet_self.write(i + 1, col_count, self_difference)

        acc_results = accomplice_manipulation(mpref, wpref, manipulator, -1)
        rank_of_acc_partner = get_w_rank(manipulator, wpref, acc_results[0])
        acc_difference = rank_of_gs_partner - rank_of_acc_partner
        sheet_acc.write(i + 1, col_count, acc_difference)

        print("n =", n, "  i =", i)

    col_count += 1
    wb.save("AccompliceVsSelf_n=" + str(max_n) + ".xls")
