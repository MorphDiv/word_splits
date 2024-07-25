import myutils
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import ast
plt.style.use('scripts/rob.mplstyle')
import pprint


def setTicks(ax, labels, rotation = 0):
    ticks = []
    for i in range (len(labels)):
        ticks.append(i + .6)

    ax.xaxis.set_major_locator(mpl.ticker.LinearLocator(len(labels)+1))
    ax.xaxis.set_minor_locator(mpl.ticker.FixedLocator(ticks))

    ax.xaxis.set_major_formatter(mpl.ticker.NullFormatter())
    ax.xaxis.set_minor_formatter(mpl.ticker.FixedFormatter(labels))

    for tick in ax.xaxis.get_minor_ticks():
        tick.tick1line.set_markersize(0)
        tick.tick2line.set_markersize(0)
        tick.label1.set_horizontalalignment('right')
        tick.label1.set_rotation(rotation)



def avg(items):
    items = [float(x) for x in items if x != '--']
    return sum(items)/len(items)

def dataset2boxplot(datasets, setting):
    print(str(datasets )+ '-' + setting)
    
    result_dir = 'symmetry_proportions_' + setting + '/'
    boxplots = {}
    for dataset in datasets:
        for line in open(result_dir + dataset + '/symmetric.txt'):
            tok = line.strip().split('\t')
            method = tok[1]
            lang = tok[2]
            buckets = tok[-4:]
            if method not in boxplots:
                boxplots[method] = [buckets]
            else:
                boxplots[method].append(buckets)

    
    expected = [[],[],[], []]
    for dataset in datasets:
        for line in open(result_dir + dataset + '/expected.txt'):
            lang, bucket, distr_str = line.strip().split('\t')
            distr = ast.literal_eval(distr_str)
            expected[int(bucket)].extend(distr)

    baseline_boxplots = {}
    for dataset in datasets:
        for line in open(result_dir + dataset + '/symmetric_baselines.txt'):
            tok = line.strip().split('\t')
            dataset, method, lang, seed = tok[:4]
            buckets = tok[-4:]
            if method not in baseline_boxplots:
                baseline_boxplots[method] = [buckets]
            else:
                baseline_boxplots[method].append(buckets)

    fig, ax = plt.subplots(figsize=(8,5), dpi=300)
    colors = ['e899ea', 'c080c2', '775178', 'a0ebea', '86c3c2', '33a75e']
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
        positions = [.125+i + methodIdx * .15 for i in range(len(observed))]
        ax.bar(positions, observed, width=.15, label=myutils.names[methodIdx], linewidth=1, edgecolor='black')
        if methodIdx == len(myutils.settings)-1:
            ax.bar(positions, baseline, width=.075, color='grey', alpha=.5, linewidth=1, edgecolor='black', label='baseline')
        else:
            ax.bar(positions, baseline, width=.075, color='grey', alpha=.5, linewidth=1, edgecolor='black')


    #plt.xticks(range(4))
    #ax.set_xticklabels(['4-8', '8-12', '12-16', '16-'])
    setTicks(ax, ['4-8', '8-12', '12-16', '16-'])
    ax.plot([0,5], [0,0], color='black')#, alpha=.8, linewidth=.8)

    ax.set_xlim((0,4))
    ax.set_ylabel('% symmetry vs expected')
    ax.set_xlabel('Buckets')
    ax.set
    leg = ax.legend()
    leg.get_frame().set_linewidth(1.5)
    fig.savefig('boxplots-' + datasets[0] + '-' + setting + '.pdf', bbox_inches='tight')
    exit(1)
#dataset2boxplot('aalto_3lang', 'strict')

#for dataset in myutils.datasets:
dataset2boxplot(['aalto_3lang'], 'strict')
dataset2boxplot(['hr_19lang', 'lr_13lang'], 'strict')
#dataset2boxplot(dataset, 'notstrict')
