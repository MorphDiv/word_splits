df <- read.csv('../baseline_files/aalto_3lang/aalto_angle_real_vs_random.csv', sep='\t')
df
setting <- 'Manual'

df1 <- df[df$fill == setting & df$setting == setting,]
df2 <- df[df$fill == 'Baseline' & df$setting == setting,]
wilcox.test(df1$angle, df2$angle, paired = TRUE)

df2
t.test(df1$angle, df2$angle, paired = TRUE)
