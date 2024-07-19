import myutils
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import ast
plt.style.use('scripts/rob.mplstyle')
import pprint

def avg(items):
    items = [float(x) for x in items if x != '--']
    return sum(items)/len(items)

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

    expected = [[],[],[],[], []]
    for line in open(result_dir + dataset + '/expected.txt'):
        lang, bucket, distr_str = line.strip().split('\t')
        distr = ast.literal_eval(distr_str)
        expected[int(bucket)].extend(distr)

    baseline_boxplots = {}
    for line in open(result_dir + dataset + '/symmetric_baselines.txt'):
        tok = line.strip().split('\t')
        dataset, method, lang, seed = tok[:4]
        buckets = tok[5:]
        if method not in baseline_boxplots:
            baseline_boxplots[method] = [buckets]
        else:
            baseline_boxplots[method].append(buckets)


    fig, ax = plt.subplots(figsize=(8,5), dpi=300)
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    colors = colors+colors
    for methodIdx, method in enumerate(myutils.settings):
        if method not in boxplots:
            continue
        # transpose
        observed = list(map(list, zip(*boxplots[method])))
        baseline = list(map(list, zip(*baseline_boxplots[method])))
        # observed = [buckets, numlangs]
        # baseline = [buckets, numlangs*seeds]
        # expected = [buckets, words]
        for bucket_idx in range(len(observed)):
            observed[bucket_idx] = (avg(observed[bucket_idx]) - avg(expected[bucket_idx])) / avg(expected[bucket_idx])
            baseline[bucket_idx] = (avg(baseline[bucket_idx]) - avg(expected[bucket_idx])) / avg(baseline[bucket_idx])
        positions = [.12+i + methodIdx * .12 for i in range(len(observed))]
        bp = ax.bar(positions, observed, width=.12, label=method)
        bp = ax.bar(positions, baseline, width=.06, color='grey', alpha=.5)


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
