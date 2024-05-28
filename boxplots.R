library(ggplot2)

df <- read.csv('random_baselines/aalto_3lang/5_random_seeds/aalto_5seeds.csv', sep='\t')

df
df$setting <- factor(df$setting, levels = c('BPE-MR', 'BPE-V', 'WP', 'SPM', 'Morfessor', 'Manual'))
df$fill <- factor(df$fill,  levels = c('BPE-MR', 'BPE-V', 'WP', 'SPM', 'Morfessor', 'Manual', 
                                       'Baseline1', 'Baseline2', 'Baseline3', 'Baseline4', 'Baseline5'))


pal1 <- 'plum2'
pal2 <- 'plum3'
pal3 <- 'plum4'
pal4 <- 'paleturquoise2'
pal5 <- 'paleturquoise3'
pal6 <- 'mediumseagreen'

pal7 <- 'gray90'
pal8 <- 'gray80'
pal9 <- 'gray70'
pal10 <- 'gray60'
pal11 <- 'gray50'

ggplot(data = df,
       aes(x = as.factor(setting), y = angle, fill = fill)) +
  geom_boxplot() +
  # geom_point() +
  # geom_text(label = df$language, hjust = 0, nudge_x = 0.1) +
  scale_y_continuous(limits = c(25, 130)) +
  scale_x_discrete(labels = c('BPE-MR', 'BPE-V', 'WP', 'SPM', 'Morfessor', 'Manual')) +
  scale_fill_manual(labels = c('BPE-MR', 'BPE-V', 'WP', 'SPM', 'Morfessor', 'Manual', 
                               'Baseline1', 'Baseline2', 'Baseline3', 'Baseline4', 'Baseline5'),
                    values = c(pal1, pal2, pal3, pal4, pal5, pal6, 
                               pal7, pal8, pal9, pal10, pal11)) +
  # geom_vline(xintercept = 5.5, linetype='dashed') +
  labs(y = 'KDE upper angle', fill='Settings', x='',
       title = '3 languages, Aalto dataset, 5 random seeds',
       # title = '19 high-resource vs. 13 manually segmented languages'
       ) +
  theme(axis.text = element_text(size = 19),
        axis.title.x = element_text(size = 21),
        axis.title.y = element_text(size = 21),
        legend.text = element_text(size = 19),
        legend.title = element_text(size = 21))

