from PlottingTools import *
import xlrd

# INITIALIZE VARIABLES BEFORE RUNNING
xls_filename = "RegretVsImprovement_n=40.xls"
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


def create_regret_vs_improvement_boxplot(improvement, regret, file_name):
    width = 0.7
    linethickness = 1.67
    font = {'size': 40, 'weight': 'bold', 'stretch': 'extra-condensed'}
    plt.style.use('seaborn-pastel')
    plt.rc('axes', axisbelow=True)
    plt.rc('font', **font)

    bpi_fliers = dict(markerfacecolor='C0', markeredgecolor='black', markersize=7, markeredgewidth=linethickness / 1.25)
    bpr_fliers = dict(markerfacecolor='C1', markeredgecolor='black', markersize=7, markeredgewidth=linethickness / 1.25)
    bpi = plt.boxplot(improvement, positions=np.array(range(len(improvement))) * 2, widths=width, flierprops=bpi_fliers, patch_artist=True)
    bpr = plt.boxplot(regret, positions=np.array(range(len(regret))) * 2, widths=width, flierprops=bpr_fliers, patch_artist=True)
    set_box_color(bpi, 'C0', linethickness, '/')
    set_box_color(bpr, 'C1', linethickness, '.')
    plt.bar([0], [0], width, label="Improvement for manipulator", color="C0", edgecolor="black", linewidth=linethickness, hatch="/")
    plt.bar([0], [0], width, label="Regret for accomplice", color="C1", edgecolor="black", linewidth=linethickness, hatch=".")
    plt.legend(loc='upper left', fancybox=True, framealpha=0.5)

    plt.xlabel("Number of men/women (n)", fontdict=font)
    plt.ylabel("Rank difference", fontdict=font)
    plt.grid(linestyle='dotted', linewidth=linethickness * 1.5)
    x_axis_ticks = get_ticks_labels(min_x, max_x, interval_x, x_axis_label_skip)
    plt.xticks(range(0, len(x_axis_ticks) * 2, 2), x_axis_ticks)
    plt.xlim(-2, len(x_axis_ticks) * 2)
    plt.axhline(y=0, color="black", linewidth=linethickness)

    figure = plt.gcf()
    ax = figure.gca()
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(linethickness)
    ax.xaxis.set_tick_params(width=linethickness)
    ax.yaxis.set_tick_params(width=linethickness)

    figure.set_figheight(10)
    figure.set_figwidth(20)
    plt.savefig(file_name, bbox_inches='tight', dpi=250)
    plt.clf()


# Get data from the xls file and create plot using the data
wb = xlrd.open_workbook(xls_filename)
improvement_max_for_w = get_data_from_xls_file(wb.sheet_by_index(0))
regret_max_for_w = get_data_from_xls_file(wb.sheet_by_index(1))
improvement_min_for_m = get_data_from_xls_file(wb.sheet_by_index(2))
regret_min_for_m = get_data_from_xls_file(wb.sheet_by_index(3))
create_regret_vs_improvement_boxplot(improvement_max_for_w, regret_max_for_w, xls_filename[:-4] + "_MaximizeImprovement.pdf")
create_regret_vs_improvement_boxplot(improvement_min_for_m, regret_min_for_m, xls_filename[:-4] + "_MinimizeRegret.pdf")
