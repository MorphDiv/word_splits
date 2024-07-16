import myutils
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import ast
plt.style.use('scripts/rob.mplstyle')


def dataset2boxplot(dataset, setting):
    print(dataset + '-' + setting)
    
    result_dir = 'symmetry_proportions_' + setting + '/'
    boxplots = {}
    for line in open(result_dir + dataset + '/symmetric.txt'):
        tok = line.strip().split('\t')
        method = tok[1]
        lang = tok[2]
        buckets = tok[-5:]
        if method not in boxplots:
            boxplots[method] = [buckets]
        else:
            boxplots[method].append(buckets)

    random = [[],[],[],[], []]
    for line in open(result_dir + dataset + '/expected.txt'):
        lang, bucket, distr_str = line.strip().split('\t')
        distr = ast.literal_eval(distr_str)
        random[int(bucket)].extend(distr)

    baseline_boxplots = {}
    for line in open(result_dir + dataset + '/symmetric_baselines.txt'):
        tok = line.strip().split('\t')
        dataset, method, lang, seed = tok[:4]
        buckets = tok[5:]
        if method not in baseline_boxplots:
            baseline_boxplots[method] = [buckets]
        else:
            baseline_boxplots[method].append(buckets)

    # transpose, because the others are also like that (will be transposed back later)
    boxplots['expected'] = list(map(list, zip(*random)))

    fig, ax = plt.subplots(figsize=(8,5), dpi=300)
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    colors = colors+colors
    for methodIdx, method in enumerate(myutils.settings + ['expected']):
        if method not in boxplots:
            continue
        # transpose
        data = list(map(list, zip(*boxplots[method])))
        if method != 'expected':
            baseline_data = list(map(list, zip(*baseline_boxplots[method])))
        # remove empty items
        for i in range(len(data)):
            for j in reversed(range(len(data[i]))):
                if data[i][j] == '--':
                    del data[i][j]
                else:
                    data[i][j] = float(data[i][j])
        if method != 'expected':
            for i in range(len(baseline_data)):
                for j in reversed(range(len(baseline_data[i]))):
                    if baseline_data[i][j] == '--':
                        del baseline_data[i][j]
                    else:
                        baseline_data[i][j] = float(baseline_data[i][j])

        positions = [.12+i + methodIdx * .12 for i in range(len(data))]
        bp = ax.boxplot(data, positions=positions, patch_artist=True, widths=.12, label=method)
        if method != 'expected':
            bp2 = ax.boxplot(baseline_data, positions=positions, patch_artist=True, widths=.06)

        edge_color = 'black'
        fill_color = colors[methodIdx]

        for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
            plt.setp(bp[element], color=edge_color)
            if method != 'expected':
                plt.setp(bp2[element], color=edge_color)
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(fill_color)
        if method != 'expected':
            for patch, color in zip(bp2['boxes'], colors):
                patch.set_facecolor(fill_color)
        plt.xticks(range(6))
        ax.set_xticklabels(['' for _ in range(6)])

    
    ax.set_xlim((0,5))
    leg = ax.legend()
    leg.get_frame().set_linewidth(1.5)
    fig.savefig('boxplots-' + dataset + '-' + setting + '.pdf', bbox_inches='tight')

#dataset2boxplot('aalto_3lang', 'strict')
for dataset in myutils.datasets:
    dataset2boxplot(dataset, 'strict')
    dataset2boxplot(dataset, 'notstrict')
