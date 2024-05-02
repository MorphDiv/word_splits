# needed for R, ggplot

with open('manual_lr/csv/total.csv', 'r') as f:
    with open('manual_lr/csv/total1.csv', 'w') as f_res:
        f_res.write('setting\tlanguage\ttotal\tseg\n')
        for line in f:
            if 'setting' not in line:
                items = line.strip().split('\t')
                print(items)
                setting = items[0]
                lang = items[1]
                # if lang == 'eng':
                #     lang = 'english'
                j = 2
                for i in range(4, 11):
                    result = setting + '\t' + lang + '\t' + items[j] + '\t' + 'seg_' + str(i)
                    f_res.write(result + '\n')
                    j += 1
