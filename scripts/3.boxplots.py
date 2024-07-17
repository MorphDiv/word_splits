import myutils
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import ast
plt.style.use('scripts/rob.mplstyle')
import pprint

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
    for methodIdx, method in enumerate(myutils.settings):
        if method not in boxplots:
            continue
        # transpose
        data = list(map(list, zip(*boxplots[method])))
        baseline_data = list(map(list, zip(*baseline_boxplots[method])))
        # subtract
        for i in range(len(data)):
            for j in reversed(range(len(data[i]))):
                if data[i][j] == '--' or baseline_data[i][j] == '--':
                    del data[i][j]
                else:
                    print(data[i][j], baseline_data[i][j])
                    data[i][j] = float(data[i][j])-float(baseline_data[i][j])
        print(data)
        positions = [.12+i + methodIdx * .12 for i in range(len(data))]
        bp = ax.boxplot(data, positions=positions, patch_artist=True, widths=.12, label=method)
        edge_color = 'black'
        fill_color = colors[methodIdx]

        for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
            plt.setp(bp[element], color=edge_color)
        for patch, color in zip(bp['boxes'], colors):
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
