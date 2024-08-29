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

fig, ax = plt.subplots(figsize=(8,5), dpi=300) 

scores = {}
for line in open('random_baselines_hr_19lang.csv').readlines()[1:] + open('random_baselines_lr_13lang.csv').readlines()[1:]:
    tok = line.strip().split(',')
    method = tok[3].replace('"', '')
    if method not in scores:
        scores[method] = {}
    lang = tok[0].replace('"', '')
    if lang not in scores[method]:
        scores[method][lang] = []
    score = float(tok[1].replace('"',''))
    scores[method][lang].append(score)

# this takes the average of each language first
#for method in scores:
#    for lang in scores[method]:
#        avg = sum(scores[method][lang])/len(scores[method][lang])
#        scores[method][lang] = avg
#for method in scores:
#    scores[method] = scores[method].values()

# Combine all seeds and all languages in 1 list
for method in scores:
    scores[method] = [j for i in scores[method].values() for j in i]


for setting_idx, setting in enumerate(myutils.settings):
    print(scores[setting])
    bp = ax.boxplot(scores[setting], positions=[setting_idx], patch_artist=True, widths=.8, label=myutils.names[setting_idx])
    edge_color = 'black'
    fill_color = myutils.colors[setting_idx]
    for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
        plt.setp(bp[element], color=edge_color)
    for patch, color in zip(bp['boxes'], myutils.colors):
        patch.set_facecolor(fill_color)



#ax.set_xticks([0,1,2])
#setTicks(ax, ['English', 'Finnish', 'Turkish'])

ax.set_ylim([0,135])
leg = ax.legend(bbox_to_anchor=(1.05, 1),loc='upper left')
leg.get_frame().set_linewidth(1.5)
fig.savefig('eveness-teddi.pdf', bbox_inches='tight')

    
