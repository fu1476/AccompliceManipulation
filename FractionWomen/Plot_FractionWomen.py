from PlottingTools import *
import xlrd

# INITIALIZE VARIABLES BEFORE RUNNING
xls_filename = "FractionWomen_n=40.xls"
iterations = 1000
min_x = 3
max_x = 40
interval_x = 1
x_axis_label_skip = 4


def get_data_from_xls_file(sheet):
    accomplice_data = []
    self_data = []
    for i in range(1, sheet.nrows):
        accomplice_data.append(float(sheet.cell_value(i, 1)))
        self_data.append(float(sheet.cell_value(i, 2)))
    return accomplice_data, self_data


# Get data from the xls file
wb = xlrd.open_workbook(xls_filename)
accomplice_wf, self_wf = get_data_from_xls_file(wb.sheet_by_index(0))
accomplice_mi, self_mi = get_data_from_xls_file(wb.sheet_by_index(1))

# Create plots from the data
x_axis_ticks = get_ticks_labels(min_x, max_x, interval_x, x_axis_label_skip)
x_axis_label = "Number of men/women (n)"
bar_labels = ["Accomplice manipulation", "Self manipulation"]
font = {'size': 35, 'weight': 'bold', 'stretch': 'extra-condensed'}
linethickness = 1.67

img_filename = xls_filename[:-4] + ".pdf"
y_axis_label = "Fraction of women"
create_histogram([accomplice_wf, self_wf], x_axis_ticks, x_axis_label, y_axis_label, bar_labels, img_filename, font=font, linethickness=linethickness)

img_filename = xls_filename[:-4] + "_ManipulableInstances.pdf"
y_axis_label = "Fraction of instances"
create_histogram([accomplice_mi, self_mi], x_axis_ticks, x_axis_label, y_axis_label, bar_labels, img_filename, font=font, linethickness=linethickness)
