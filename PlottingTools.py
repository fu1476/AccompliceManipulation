import matplotlib.pyplot as plt
import numpy as np

HATCHES_GLOBAL = ["/", ".", "x", "-", "*", "O"]
FONT_GLOBAL = {'size': 30}


def get_ticks_labels(min_x, max_x, interval, skip):
    labels = []
    for x in range(min_x, max_x + 1, interval):
        if x % skip == 0:
            labels.append(str(x))
        else:
            labels.append("")
    return labels


def create_histogram_single_category(data, x_axis_ticks, x_axis_label, y_axis_label, filename, width=0.7, figheight=10, figwidth=20, linethickness=1, font=None):
    if font is None:
        font = FONT_GLOBAL
    plt.style.use('seaborn-pastel')
    plt.rc('axes', axisbelow=True)
    plt.rc('font', **font)
    b = range(len(data))
    plt.bar(b, data, width, edgecolor='black', linewidth=linethickness)
    plt.xlim(-0.66, len(x_axis_ticks) - 0.33)
    plt.xticks(b, x_axis_ticks)
    plt.xlabel(x_axis_label, fontdict=font)
    plt.ylabel(y_axis_label, fontdict=font)
    plt.grid(linestyle='dotted', linewidth=linethickness * 1.5)
    figure = plt.gcf()
    ax = figure.gca()
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(linethickness)
    ax.xaxis.set_tick_params(width=linethickness)
    ax.yaxis.set_tick_params(width=linethickness)
    figure.set_figheight(figheight)
    figure.set_figwidth(figwidth)
    plt.savefig(filename, bbox_inches='tight', dpi=250)
    plt.clf()


def plot_bars(data, bar_labels, width, hatches, linethickness):
    categories_count = len(data)
    _X = np.arange(len(data[0]))
    for i in range(categories_count):
        plt.bar(_X - width / 2. + i / float(categories_count) * width, data[i], width / float(categories_count), hatch=hatches[i], edgecolor="black", linewidth=linethickness, align="edge", label=bar_labels[i])


def create_histogram(data, x_axis_ticks, x_axis_label, y_axis_label, bar_labels, filename, width=0.7, figheight=10, figwidth=20, linethickness=1, hatches=None, font=None, y_ticks=None, y_range=None):
    if hatches is None:
        hatches = HATCHES_GLOBAL
    if font is None:
        font = FONT_GLOBAL
    plt.style.use('seaborn-pastel')
    plt.rc('axes', axisbelow=True)
    plt.rc('font', **font)
    plot_bars(data, bar_labels, width, hatches, linethickness)
    plt.legend(loc='upper left', fancybox=True, framealpha=0.5)
    plt.xlim(-0.66, len(x_axis_ticks) - 0.33)
    plt.xticks(range(len(x_axis_ticks)), x_axis_ticks)
    if y_ticks is not None:
        plt.yticks(y_ticks)
    plt.xlabel(x_axis_label, fontdict=font)
    plt.ylabel(y_axis_label, fontdict=font)
    plt.grid(linestyle='dotted', linewidth=linethickness * 1.5)
    figure = plt.gcf()
    ax = figure.gca()
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(linethickness)
    ax.xaxis.set_tick_params(width=linethickness)
    ax.yaxis.set_tick_params(width=linethickness)
    if y_range is not None:
        ax.set_ylim(y_range)
    figure.set_figheight(figheight)
    figure.set_figwidth(figwidth)
    plt.savefig(filename, bbox_inches='tight', dpi=250)
    plt.clf()


def set_box_color(bp, bp_color, linethickness, hatch=None):
    plt.setp(bp['whiskers'], color='black', linewidth=linethickness)
    plt.setp(bp['caps'], color='black', linewidth=linethickness)
    plt.setp(bp['medians'], color='black', linewidth=linethickness * 1.5)
    for idx, box in enumerate(bp['boxes']):
        box.set(color='black', linewidth=linethickness)
        box.set(facecolor=bp_color)
        if hatch is not None:
            box.set(hatch=hatch)


def create_boxplot(data, x_axis_ticks, x_axis_label, y_axis_label, filename, width=0.7, figheight=10, figwidth=20, linethickness=1, font=None, include_outliers=True):
    if font is None:
        font = FONT_GLOBAL
    plt.style.use('seaborn-pastel')
    plt.rc('axes', axisbelow=True)
    plt.rc('font', **font)
    bp_fliers = dict(markerfacecolor='C0', markeredgecolor='black', markersize=7, markeredgewidth=linethickness / 1.25)
    bp = plt.boxplot(data, positions=np.array(range(len(data))), widths=width, flierprops=bp_fliers, patch_artist=True, showfliers=include_outliers)
    set_box_color(bp, 'C0', linethickness)
    plt.xlim(-0.66, len(x_axis_ticks) - 0.33)
    plt.xticks(range(len(x_axis_ticks)), x_axis_ticks)
    plt.xlabel(x_axis_label, fontdict=font)
    plt.ylabel(y_axis_label, fontdict=font)
    plt.grid(linestyle='dotted', linewidth=linethickness * 1.5)
    figure = plt.gcf()
    ax = figure.gca()
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(linethickness)
    ax.xaxis.set_tick_params(width=linethickness)
    ax.yaxis.set_tick_params(width=linethickness)
    figure.set_figheight(figheight)
    figure.set_figwidth(figwidth)
    plt.savefig(filename, bbox_inches='tight', dpi=250)
    plt.clf()


def create_boxplot_two_categories(data, x_axis_ticks, x_axis_label, y_axis_label, box_labels, filename, width=0.7, figheight=10, figwidth=20, linethickness=1, hatches=None, font=None, include_outliers=True):
    if hatches is None:
        hatches = HATCHES_GLOBAL
    if font is None:
        font = FONT_GLOBAL
    plt.style.use('seaborn-pastel')
    plt.rc('axes', axisbelow=True)
    plt.rc('font', **font)
    box_gap = 0.1
    box_width = (width - box_gap) / 2
    bp0_fliers = dict(markerfacecolor='C0', markeredgecolor='black', markersize=7, markeredgewidth=linethickness / 1.25)
    bp1_fliers = dict(markerfacecolor='C1', markeredgecolor='black', markersize=7, markeredgewidth=linethickness / 1.25)
    bp0 = plt.boxplot(data[0], positions=np.array(range(len(data[0]))) - (box_width + box_gap) / 2, widths=box_width, flierprops=bp0_fliers, patch_artist=True, showfliers=include_outliers)
    bp1 = plt.boxplot(data[1], positions=np.array(range(len(data[1]))) + (box_width + box_gap) / 2, widths=box_width, flierprops=bp1_fliers, patch_artist=True, showfliers=include_outliers)
    set_box_color(bp0, 'C0', linethickness, hatches[0])
    set_box_color(bp1, 'C1', linethickness, hatches[1])
    plt.bar([0], [0], 0, label=box_labels[0], color='C0', edgecolor='black', linewidth=linethickness, hatch=hatches[0])
    plt.bar([0], [0], 0, label=box_labels[1], color='C1', edgecolor='black', linewidth=linethickness, hatch=hatches[1])
    plt.legend(loc='upper left', fancybox=True, framealpha=0.5)
    plt.xlim(-0.66, len(x_axis_ticks) - 0.33)
    plt.xticks(np.array(range(len(x_axis_ticks))), x_axis_ticks)
    plt.xlabel(x_axis_label, fontdict=font)
    plt.ylabel(y_axis_label, fontdict=font)
    plt.grid(linestyle='dotted', linewidth=linethickness * 1.5)
    figure = plt.gcf()
    ax = figure.gca()
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(linethickness)
    ax.xaxis.set_tick_params(width=linethickness)
    ax.yaxis.set_tick_params(width=linethickness)
    figure.set_figheight(figheight)
    figure.set_figwidth(figwidth)
    plt.savefig(filename, bbox_inches='tight', dpi=250)
    plt.clf()


def create_boxplot_three_categories(data, x_axis_ticks, x_axis_label, y_axis_label, box_labels, filename, width=0.7, figheight=10, figwidth=20, linethickness=1, hatches=None, font=None, include_outliers=True):
    if hatches is None:
        hatches = HATCHES_GLOBAL
    if font is None:
        font = FONT_GLOBAL
    plt.style.use('seaborn-pastel')
    plt.rc('axes', axisbelow=True)
    plt.rc('font', **font)
    box_gap = 0.05
    box_width = (width - (box_gap) * 2) / 3

    bp0_fliers = dict(markerfacecolor='C0', markeredgecolor='black', markersize=7, markeredgewidth=linethickness / 1.25)
    bp1_fliers = dict(markerfacecolor='C1', markeredgecolor='black', markersize=7, markeredgewidth=linethickness / 1.25)
    bp2_fliers = dict(markerfacecolor='C2', markeredgecolor='black', markersize=7, markeredgewidth=linethickness / 1.25)

    bp0 = plt.boxplot(data[0], positions=np.array(range(len(data[0]))) - 3 * (box_width + box_gap) / 3, widths=box_width, flierprops=bp0_fliers, patch_artist=True, showfliers=include_outliers)
    bp1 = plt.boxplot(data[1], positions=np.array(range(len(data[1]))), widths=box_width, flierprops=bp1_fliers, patch_artist=True, showfliers=include_outliers)
    bp2 = plt.boxplot(data[2], positions=np.array(range(len(data[2]))) + 3 * (box_width + box_gap) / 3, widths=box_width, flierprops=bp2_fliers, patch_artist=True, showfliers=include_outliers)

    set_box_color(bp0, 'C0', linethickness, hatches[0])
    set_box_color(bp1, 'C1', linethickness, hatches[1])
    set_box_color(bp2, 'C2', linethickness, hatches[2])

    plt.bar([0], [0], 0, label=box_labels[0], color='C0', edgecolor='black', linewidth=linethickness, hatch=hatches[0])
    plt.bar([0], [0], 0, label=box_labels[1], color='C1', edgecolor='black', linewidth=linethickness, hatch=hatches[1])
    plt.bar([0], [0], 0, label=box_labels[2], color='C2', edgecolor='black', linewidth=linethickness, hatch=hatches[2])

    plt.legend(loc='upper left', fancybox=True, framealpha=0.5)
    plt.xlim(-0.66, len(x_axis_ticks) - 0.33)
    plt.xticks(np.array(range(len(x_axis_ticks))), x_axis_ticks)
    plt.xlabel(x_axis_label, fontdict=font)
    plt.ylabel(y_axis_label, fontdict=font)
    plt.grid(linestyle='dotted', linewidth=linethickness * 1.5)
    figure = plt.gcf()
    ax = figure.gca()
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(linethickness)
    ax.xaxis.set_tick_params(width=linethickness)
    ax.yaxis.set_tick_params(width=linethickness)
    figure.set_figheight(figheight)
    figure.set_figwidth(figwidth)
    plt.savefig(filename, bbox_inches='tight', dpi=250)
    plt.clf()


def create_boxplot_four_categories(data, x_axis_ticks, x_axis_label, y_axis_label, box_labels, filename, width=0.7, figheight=10, figwidth=20, linethickness=1, hatches=None, font=None, include_outliers=True):
    if hatches is None:
        hatches = HATCHES_GLOBAL
    if font is None:
        font = FONT_GLOBAL
    plt.style.use('seaborn-pastel')
    plt.rc('axes', axisbelow=True)
    plt.rc('font', **font)
    box_gap = 0.05
    box_width = (width - (box_gap * 3)) / 4

    bp0_fliers = dict(markerfacecolor='C0', markeredgecolor='black', markersize=7, markeredgewidth=linethickness / 1.25)
    bp1_fliers = dict(markerfacecolor='C1', markeredgecolor='black', markersize=7, markeredgewidth=linethickness / 1.25)
    bp2_fliers = dict(markerfacecolor='C2', markeredgecolor='black', markersize=7, markeredgewidth=linethickness / 1.25)
    bp3_fliers = dict(markerfacecolor='C3', markeredgecolor='black', markersize=7, markeredgewidth=linethickness / 1.25)

    bp0 = plt.boxplot(data[0], positions=np.array(range(len(data[0]))) - 6 * (box_width + box_gap) / 4, widths=box_width, flierprops=bp0_fliers, patch_artist=True, showfliers=include_outliers)
    bp1 = plt.boxplot(data[1], positions=np.array(range(len(data[1]))) - 2 * (box_width + box_gap) / 4, widths=box_width, flierprops=bp1_fliers, patch_artist=True, showfliers=include_outliers)
    bp2 = plt.boxplot(data[2], positions=np.array(range(len(data[2]))) + 2 * (box_width + box_gap) / 4, widths=box_width, flierprops=bp2_fliers, patch_artist=True, showfliers=include_outliers)
    bp3 = plt.boxplot(data[3], positions=np.array(range(len(data[3]))) + 6 * (box_width + box_gap) / 4, widths=box_width, flierprops=bp3_fliers, patch_artist=True, showfliers=include_outliers)

    set_box_color(bp0, 'C0', linethickness, hatches[0])
    set_box_color(bp1, 'C1', linethickness, hatches[1])
    set_box_color(bp2, 'C2', linethickness, hatches[2])
    set_box_color(bp3, 'C3', linethickness, hatches[3])

    plt.bar([0], [0], 0, label=box_labels[0], color='C0', edgecolor='black', linewidth=linethickness)
    plt.bar([0], [0], 0, label=box_labels[1], color='C1', edgecolor='black', linewidth=linethickness)
    plt.bar([0], [0], 0, label=box_labels[2], color='C2', edgecolor='black', linewidth=linethickness)
    plt.bar([0], [0], 0, label=box_labels[3], color='C3', edgecolor='black', linewidth=linethickness)

    plt.legend(loc='upper left', fancybox=True, framealpha=0.5)
    plt.xlim(-0.66, len(x_axis_ticks) - 0.33)
    plt.xticks(np.array(range(len(x_axis_ticks))), x_axis_ticks)
    plt.xlabel(x_axis_label, fontdict=font)
    plt.ylabel(y_axis_label, fontdict=font)
    plt.grid(linestyle='dotted', linewidth=linethickness * 1.5)
    figure = plt.gcf()
    ax = figure.gca()
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(linethickness)
    ax.xaxis.set_tick_params(width=linethickness)
    ax.yaxis.set_tick_params(width=linethickness)
    figure.set_figheight(figheight)
    figure.set_figwidth(figwidth)
    plt.savefig(filename, bbox_inches='tight', dpi=250)
    plt.clf()
