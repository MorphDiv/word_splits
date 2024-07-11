import myutils
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

plt.style.use('scripts/rob.mplstyle')


def dataset2boxplot(dataset, setting):
    result_dir = 'symmetry_proportions_' + setting + '/'
    boxplots = {}
    for line in open(result_dir + dataset + '/symmetric.txt'):
        tok = line.strip().split('\t')
        method = tok[1]
        lang = tok[2]
        buckets = [float(x) for x in tok[-5:]]
        if method not in boxplots:
            boxplots[method] = [buckets]
        else:
            boxplots[method].append(buckets)
    fig, ax = plt.subplots(figsize=(8,5), dpi=300)
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    for methodIdx, method in enumerate(boxplots):
        # transpose
        data = list(map(list, zip(*boxplots[method])))
        # remove empty items
        for i in range(len(data)):
            for j in reversed(range(len(data[i]))):
                if data[i][j] == '--':
                    del data[i][j]

        positions = [.15+i + methodIdx * .15 for i in range(len(data))]
        print(dataset,method, data)
        bp = ax.boxplot(data, positions=positions, patch_artist=True, widths=.1, label=method)

        edge_color = 'black'
        fill_color = colors[methodIdx]

        for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
            plt.setp(bp[element], color=edge_color)
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(fill_color)
        plt.xticks(range(6))

    ax.set_xlim((0,5))
    leg = ax.legend()
    leg.get_frame().set_linewidth(1.5)
    fig.savefig('boxplots-' + dataset + '-' + setting + '.pdf', bbox_inches='tight')

dataset2boxplot('aalto_3lang', 'strict')
#for dataset in myutils.datasets:
#    dataset2boxplot(dataset, 'strict')
#    dataset2boxplot(dataset, 'notstrict')
