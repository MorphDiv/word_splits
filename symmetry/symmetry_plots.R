library(ggplot2)
library(gganimate)
library(reshape2)

df <- read.csv('../symmetry_results/hr_19lang/csv/proportions1.csv', sep = '\t')
df_total <- read.csv('../symmetry_results/hr_19lang/csv/total1.csv', sep = '\t')

df$total <- df_total$total

new_df <- subset(df, total > 0)

df1 <- new_df[new_df$setting == "HR, bpe200",]
df1 <- df1[df1$language %in% c('japanese', 'korean', 'mandarin', 'persian', 'hindi', 'indonesian',
                               'thai', 'vietnamese', 'hebrew_modern', 'turkish', 'tagalog'),]

ggplot(df1, aes(x = factor(seg), y = proportion, color = language, group = language)) +
  geom_point() +
  geom_line() +
  scale_x_discrete(limits = c('seg_4', 'seg_5', 'seg_6', 'seg_7', 'seg_8', 'seg_9', 'seg_10')) +
  labs(title = df1$setting)
