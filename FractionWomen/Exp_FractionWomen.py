from AccompliceManipulation import *
from SelfManipulation import *
from GenerateRandomMarriageInstance import *
from xlwt import Workbook

# INITIALIZE VARIABLES BEFORE RUNNING
iterations = 1000
min_n = 3
max_n = 40

wb = Workbook()
sheet_women_fraction = wb.add_sheet("Women fraction")
sheet_women_fraction.write(0, 0, "n")
sheet_women_fraction.write(0, 1, "Accomplice")
sheet_women_fraction.write(0, 2, "Self")
sheet_manipulable_instances = wb.add_sheet("Manipulable instances fraction")
sheet_manipulable_instances.write(0, 0, "n")
sheet_manipulable_instances.write(0, 1, "Accomplice")
sheet_manipulable_instances.write(0, 2, "Self")
sheet_accomplice_counts = wb.add_sheet("Accomplice counts")
sheet_self_counts = wb.add_sheet("Self counts")
for x in range(max_n + 1):
    sheet_accomplice_counts.write(0, x + 1, x)
    sheet_self_counts.write(0, x + 1, x)

self_list = []
accomplice_list = []

self_manipulable_list = []
accomplice_manipulable_list = []

for n in range(min_n, max_n + 1):
    self_count = 0
    accomplice_count = 0
    self_manipulable_count = 0
    accomplice_manipulable_count = 0
    self_count_i_list = [0 for i in range(n + 1)]
    accomplice_count_i_list = [0 for i in range(n + 1)]

    for i in range(iterations):
        self_count_i = 0
        accomplice_count_i = 0

        mpref, wpref = generate_uniform(n)
        gs_matches = gale_shapley(mpref, wpref)

        for manipulator in range(1, n + 1):
            gs_partner = gs_matches.index(manipulator) + 1
            rank_of_gs_partner = wpref[manipulator - 1].index(gs_partner) + 1

            accomplice_results = accomplice_manipulation(mpref, wpref, manipulator, -1)
            accomplice_partner = accomplice_results[0].index(manipulator) + 1
            rank_of_accomplice_partner = wpref[manipulator - 1].index(accomplice_partner) + 1
            if rank_of_accomplice_partner < rank_of_gs_partner:
                accomplice_count += 1
                accomplice_count_i += 1

            self_results = self_manipulation(mpref, wpref, manipulator)
            self_partner = self_results[0].index(manipulator) + 1
            rank_of_self_partner = wpref[manipulator - 1].index(self_partner) + 1
            if rank_of_self_partner < rank_of_gs_partner:
                self_count += 1
                self_count_i += 1

        print("n =", n, "i =", i)

        self_count_i_list[self_count_i] += 1
        accomplice_count_i_list[accomplice_count_i] += 1

        if self_count_i > 0:
            self_manipulable_count += 1
        if accomplice_count_i > 0:
            accomplice_manipulable_count += 1

    sheet_accomplice_counts.write(n - min_n + 1, 0, n)
    sheet_self_counts.write(n - min_n + 1, 0, n)
    for x in range(len(self_count_i_list)):
        sheet_accomplice_counts.write(n - min_n + 1, x + 1, accomplice_count_i_list[x])
        sheet_self_counts.write(n - min_n + 1, x + 1, self_count_i_list[x])

    self_list.append(self_count / iterations / n)
    accomplice_list.append(accomplice_count / iterations / n)
    self_manipulable_list.append(self_manipulable_count / iterations)
    accomplice_manipulable_list.append(accomplice_manipulable_count / iterations)

    sheet_women_fraction.write(n - min_n + 1, 0, n)
    sheet_women_fraction.write(n - min_n + 1, 1, accomplice_count / iterations / n)
    sheet_women_fraction.write(n - min_n + 1, 2, self_count / iterations / n)

    sheet_manipulable_instances.write(n - min_n + 1, 0, n)
    sheet_manipulable_instances.write(n - min_n + 1, 1, accomplice_manipulable_count / iterations)
    sheet_manipulable_instances.write(n - min_n + 1, 2, self_manipulable_count / iterations)

    wb.save("FractionWomen_n=" + str(max_n) + ".xls")
