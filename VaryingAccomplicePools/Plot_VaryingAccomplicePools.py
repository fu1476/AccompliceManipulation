from PlottingTools import *
import xlrd

# INITIALIZE VARIABLES BEFORE RUNNING
xls_filename = "VaryingAccomplicePools_n=40.xls"
iterations = 1000


def create_stacked_histogram(sheet_index):
    width = 0.7
    linethickness = 1.67
    font = {'size': 35, 'weight': 'bold', 'stretch': 'extra-condensed'}
    plt.style.use('seaborn-pastel')
    plt.rc('axes', axisbelow=True)
    plt.rc('font', **font)

    nr_beats_gs_list = []
    wr_beats_gs_list = []
    sheet = wb.sheet_by_index(sheet_index)
    for i in range(1, sheet.nrows):
        nr_beats_gs_list.append(float(sheet.cell_value(i, 2)))
        wr_beats_gs_list.append(float(sheet.cell_value(i, 3)) - float(sheet.cell_value(i, 2)))
    self_beats_gs = sheet.cell_value(1, 1)

    n = len(nr_beats_gs_list)
    b = np.arange(n)
    plt.bar(b, nr_beats_gs_list, width, label="No-regret accomplice beats truth telling", color="C0", edgecolor="black", linewidth=linethickness, hatch="/")
    plt.bar(b, wr_beats_gs_list, width, bottom=nr_beats_gs_list, label="With-regret accomplice beats truth telling", color="C1", edgecolor="black", linewidth=linethickness, hatch=".")
    plt.plot([], c="black", label="Self beats truth telling")

    axes = plt.gca()
    axes.set_ylim([0, 1])
    handles, labels = axes.get_legend_handles_labels()
    handles = [handles[1], handles[2], handles[0]]
    labels = [labels[1], labels[2], labels[0]]
    plt.legend(handles, labels, loc='upper left', fancybox=True, framealpha=0.5)

    plt.xlabel("Size of the pool of potential accomplices (p)", fontdict=font)
    plt.ylabel("Fraction of instances", fontdict=font)
    x_axis_ticks = get_ticks_labels(1, n, 1, n // 10)
    plt.xticks(range(len(x_axis_ticks)), x_axis_ticks)
    plt.yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    plt.margins(x=0.01)
    plt.grid(linestyle='dotted', linewidth=linethickness * 1.5)
    plt.axhline(y=self_beats_gs, color="black", linewidth=3)

    figure = plt.gcf()
    ax = figure.gca()
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(linethickness)
    ax.xaxis.set_tick_params(width=linethickness)
    ax.yaxis.set_tick_params(width=linethickness)

    figure.set_figheight(10)
    figure.set_figwidth(20)
    plt.savefig(f"VaryingAccomplicePools_n={str(n)}.pdf", bbox_inches='tight', dpi=250)
    plt.clf()


# Create plots for each sheet in the xls file
wb = xlrd.open_workbook(xls_filename)
for i in range(len(wb.sheet_names())):
    create_stacked_histogram(i)
