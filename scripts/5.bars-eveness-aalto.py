import myutils
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('scripts/rob.mplstyle')

def setTicks(ax, labels, rotation = 0):
    ticks = []
    for i in range (len(labels)):
        ticks.append(i + .5)

    ax.xaxis.set_major_locator(mpl.ticker.LinearLocator(len(labels)+1))
    ax.xaxis.set_minor_locator(mpl.ticker.FixedLocator(ticks))
    
    ax.xaxis.set_major_formatter(mpl.ticker.NullFormatter())
    ax.xaxis.set_minor_formatter(mpl.ticker.FixedFormatter(labels))
        
    for tick in ax.xaxis.get_minor_ticks():
        tick.tick1line.set_markersize(0)
        tick.tick2line.set_markersize(0)
        tick.label1.set_horizontalalignment('right')
        tick.label1.set_rotation(rotation)



scores = {}
baselines = {}
for line in open('upper_angle_values/aalto_3lang_angle_real_vs_random_5seeds.csv').readlines()[1:]:
    lang, angle, base, method = line.strip().split('\t')
    if base.startswith("Baseline"):
        if method not in baselines:
            baselines[method] = {}
        if lang not in baselines[method]:
            baselines[method][lang] = []
        baselines[method][lang].append(float(angle))
    else:
        if method not in scores:
            scores[method] = {}
        scores[method][lang] = float(angle)



fig, ax = plt.subplots(figsize=(8,5), dpi=300)
for methodIdx, method in enumerate(myutils.names):
    observed = [scores[method][lang] for lang in ['English', 'Finnish', 'Turkish']]
    baseline = [baselines[method][lang] for lang in ['English', 'Finnish', 'Turkish']]
    baseline = [sum(x)/len(x) for x in baseline]
    positions = [.125+ i + methodIdx * .15 for i in range(len(observed))]
    #positions[0] = positions[0]-.2
    avg_observed = sum(observed)/len(observed)
    avg_baseline = sum(baseline)/len(baseline)
    
    ax.bar([methodIdx], avg_observed, color=myutils.colors[methodIdx], label=method)
    ax.plot([methodIdx-.39, methodIdx+.39], [avg_baseline, avg_baseline], color='black')

ax.set_ylim([0,135])
ax.set_xticks(range(len(myutils.names)))
ax.set_xticklabels(myutils.names)
#setTicks(ax, myutils.names)

#leg = ax.legend()
#leg.get_frame().set_linewidth(1.5)
fig.savefig('eveness-aalto.pdf', bbox_inches='tight')

    
