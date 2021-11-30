from PlottingTools import *
import xlrd

# INITIALIZE VARIABLES BEFORE RUNNING
xls_filename = "AccompliceVsSelf_n=40.xls"
iterations = 1000
min_x = 3
max_x = 40
interval_x = 1
x_axis_label_skip = 4


def get_data_from_xls_file(sheet):
    data = []
    for i in range(0, sheet.ncols):
        list_n = []
        for j in range(1, sheet.nrows):
            cell = sheet.cell_value(j, i)
            if cell == "":
                break
            list_n.append(int(cell))
        data.append(list_n)
    return data


# Get data from the xls file
wb = xlrd.open_workbook(xls_filename)
self = get_data_from_xls_file(wb.sheet_by_index(0))
acc = get_data_from_xls_file(wb.sheet_by_index(1))

length = len(acc)
acc_beats_gs = [len([x for x in X if x != 0]) / iterations for X in acc]
self_beats_gs = [len([x for x in X if x != 0]) / iterations for X in self]
acc_beats_self = [[1 if acc[i][j] > self[i][j] else 0 for j in range(iterations)].count(1) / iterations for i in range(length)]
self_beats_acc = [[1 if self[i][j] > acc[i][j] else 0 for j in range(iterations)].count(1) / iterations for i in range(length)]
acc_distributions = [[acc[i][j] for j in range(iterations) if acc[i][j] > 0] for i in range(length)]
self_distributions = [[self[i][j] for j in range(iterations) if self[i][j] > 0] for i in range(length)]

# Create plots from the data
x_axis_ticks = get_ticks_labels(min_x, max_x, interval_x, x_axis_label_skip)
x_axis_label = "Number of men/women (n)"
font = {'size': 45, 'weight': 'bold', 'stretch': 'extra-condensed'}
y_ticks = [0, 0.05, 0.1, 0.15, 0.2, 0.25]
y_range = [0, 0.26]
linethickness = 1.67

img_filename = xls_filename[:-4] + "_AgainstTruthTelling.pdf"
y_axis_label = "Fraction of instances"
bar_labels = ["Accomplice beats truth telling", "Self beats truth telling"]
create_histogram([acc_beats_gs, self_beats_gs], x_axis_ticks, x_axis_label, y_axis_label, bar_labels, img_filename, font=font, linethickness=linethickness, y_ticks=y_ticks, y_range=y_range)

img_filename = xls_filename[:-4] + "_AgainstEachOther.pdf"
y_axis_label = "Fraction of instances"
bar_labels = ["Accomplice beats self", "Self beats accomplice"]
create_histogram([acc_beats_self, self_beats_acc], x_axis_ticks, x_axis_label, y_axis_label, bar_labels, img_filename, font=font, linethickness=linethickness, y_ticks=y_ticks, y_range=y_range)

img_filename = xls_filename[:-4] + "_RankDifference.pdf"
y_axis_label = "Rank difference"
bar_labels = ["Accomplice", "Self"]
create_boxplot_two_categories([acc_distributions, self_distributions], x_axis_ticks, x_axis_label, y_axis_label, bar_labels, img_filename, font=font, linethickness=linethickness)
