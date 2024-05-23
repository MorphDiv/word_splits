import os
import re


def find_subarray(main_array, subarray):
    sub_len = len(subarray)
    main_len = len(main_array)

    if sub_len <= main_len:

        for i in range(main_len - sub_len + 1):
            if main_array[i:i + sub_len] == subarray:
                return True

    return False


def dict_add_pattern(array):
    global patterns_dict

    if tuple(array) not in patterns_dict:
        patterns_dict[tuple(array)] = 1
    else:
        patterns_dict[tuple(array)] += 1


settings = ['bpe-mr']

langs = ['basque', 'eng', 'finnish', 'french', 'german', 'greek_modern',
         'hebrew_modern', 'hindi', 'indonesian', 'japanese', 'korean',
         'mandarin', 'persian', 'russian', 'spanish', 'tagalog', 'thai',
         'turkish', 'vietnamese']

f_sym = open('../symmetry_proportions/hr_19lang/bpe-mr/symmetric.txt', 'w')
f_total = open('../symmetry_proportions/hr_19lang/bpe-mr/total.txt', 'w')
f_proportions = open('../symmetry_proportions/hr_19lang/bpe-mr/proportions.txt', 'w')


with open('../symmetry_results/patterns_freq/hr_19lang.txt', 'w') as f_patterns:

    for lang in langs:
        for setting in settings:
            print(lang, setting)
            f_patterns.write(lang + ' ' + setting + '\n')
            symmetric = []
            totals = []
            proportions = []
            
            patterns_dict = {}

            fname = f'../hr_19lang/{setting}/{lang}_results.csv'

            if os.path.exists(fname):
                with open(fname, 'r') as f:
                    text = f.read()

            if os.path.exists(fname):

                for l in range(4, 11):
                    # print('segments: ', l)
                    with open(fname, 'r') as f:
                        index = 0
                        translational = 0
                        reflectional = 0
                        same = 0
                        sum_all_seq = 0
                        set_lines = set()
                        for line in f:
                            if index > 0:
                                items = line.strip().split('\t')
                                num_str = items[1][1:-1]
                                arr = items[1][1:-1].split(', ')
                                arr = [int(i) for i in arr if i != '']

                                if len(arr) == l:
                                    sum_all_seq += 1
                                    # translational: 1, 2, 1, 2
                                    for i in range(1, 20):
                                        for j in range(1, 20):
                                            if i != j:
                                                if find_subarray(arr, [i, j, i, j]):
                                                # if f'{i}, {j}, {i}, {j}' in num_str:
                                                    # print(num_str)
                                                    # print(items[0])
                                                    translational += 1
                                                    set_lines.add(line)

                                                    dict_add_pattern([i, j, i, j])

                                                if find_subarray(arr, [j, i, j, i]):
                                                # if f'{j}, {i}, {j}, {i}' in num_str:
                                                    # print(num_str)
                                                    # print(items[0])
                                                    translational += 1
                                                    set_lines.add(line)

                                                    dict_add_pattern([j, i, j, i])

                                                if find_subarray(arr, [i, j, i, i, j, i]):
                                                # if f'{i}, {j}, {i}, {i}, {j}, {i}' in num_str:
                                                    # print(num_str)
                                                    # print(items[0])
                                                    translational += 1
                                                    set_lines.add(line)

                                                    dict_add_pattern([i, j, i, i, j, i])

                                                if find_subarray(arr, [j, i, j, j, i, j]):
                                                    # print(num_str)
                                                    # print(items[0])
                                                    translational += 1
                                                    set_lines.add(line)

                                                    dict_add_pattern([j, i, j, j, i, j])

                                                if find_subarray(arr, [i, i, j, i, i, j]):
                                                    # print(num_str)
                                                    # print(items[0])
                                                    translational += 1
                                                    set_lines.add(line)

                                                    dict_add_pattern([i, i, j, i, i, j])

                                                if find_subarray(arr, [j, j, i, j, j, i]):
                                                    # print(num_str)
                                                    # print(items[0])
                                                    translational += 1
                                                    set_lines.add(line)

                                                    dict_add_pattern([j, j, i, j, j, i])

                                                if find_subarray(arr, [i, j, j, i, j, j]):
                                                    # print(num_str)
                                                    # print(items[0])
                                                    translational += 1
                                                    set_lines.add(line)

                                                    dict_add_pattern([i, j, j, i, j, j])


                                                if find_subarray(arr, [j, i, i, j, i, i]):
                                                    # print(num_str)
                                                    # print(items[0])
                                                    translational += 1
                                                    set_lines.add(line)

                                                    dict_add_pattern([j, i, i, j, i, i])

                                                if find_subarray(arr, [i, i, i, j, i, i, i, j]):
                                                    # print(num_str)
                                                    # print(items[0])
                                                    translational += 1
                                                    set_lines.add(line)

                                                    dict_add_pattern([i, i, i, j, i, i, i, j])

                                                if find_subarray(arr, [j, j, j, i, j, j, j, i]):
                                                    # print(num_str)
                                                    # print(items[0])
                                                    translational += 1
                                                    set_lines.add(line)

                                                    dict_add_pattern([j, j, j, i, j, j, j, i])

                                                if find_subarray(arr, [i, j, j, j, i, j, j, j]):
                                                    # print(num_str)
                                                    # print(items[0])
                                                    translational += 1
                                                    set_lines.add(line)

                                                    dict_add_pattern([i, j, j, j, i, j, j, j])

                                                if find_subarray(arr, [j, i, i, i, j, i, i, i]):
                                                    # print(num_str)
                                                    # print(items[0])
                                                    translational += 1
                                                    set_lines.add(line)

                                                    dict_add_pattern([j, i, i, i, j, i, i, i])

                                                if find_subarray(arr, [i, i, j, i, i, i, j, i]):
                                                    # print(num_str)
                                                    # print(items[0])
                                                    translational += 1
                                                    set_lines.add(line)

                                                    dict_add_pattern([i, i, j, i, i, i, j, i])

                                                if find_subarray(arr, [j, j, i, j, j, j, i, j]):
                                                    # print(num_str)
                                                    # print(items[0])
                                                    translational += 1
                                                    set_lines.add(line)

                                                    dict_add_pattern([j, j, i, j, j, j, i, j])

                                                if find_subarray(arr, [i, j, i, i, i, j, i, i]):
                                                    # print(num_str)
                                                    # print(items[0])
                                                    translational += 1
                                                    set_lines.add(line)

                                                    dict_add_pattern([i, j, i, i, i, j, i, i])

                                                if find_subarray(arr, [j, i, j, j, j, i, j, j]):
                                                    # print(num_str)
                                                    # print(items[0])
                                                    translational += 1
                                                    set_lines.add(line)

                                                    dict_add_pattern([j, i, j, j, j, i, j, j])

                                                if find_subarray(arr, [i, j, j, i]):
                                                    # print(num_str)
                                                    reflectional += 1
                                                    set_lines.add(line)

                                                    dict_add_pattern([i, j, j, i])

                                                if find_subarray(arr, [j, i, i, j]):
                                                    # print(num_str)
                                                    reflectional += 1
                                                    set_lines.add(line)

                                                    dict_add_pattern([j, i, i, j])

                                                if find_subarray(arr, [j, i, i, i, i, j]):
                                                    # print(num_str)
                                                    reflectional += 1
                                                    set_lines.add(line)

                                                    dict_add_pattern([j, i, i, i, i, j])

                                                if find_subarray(arr, [j, j, i, i, j, j]):
                                                    # print(num_str)
                                                    reflectional += 1
                                                    set_lines.add(line)

                                                    dict_add_pattern([j, j, i, i, j, j])

                                                if find_subarray(arr, [i, j, j, j, j, i]):
                                                    # print(num_str)
                                                    reflectional += 1
                                                    set_lines.add(line)

                                                    dict_add_pattern([i, j, j, j, j, i])

                                                if find_subarray(arr, [i, i, j, j, i, i]):
                                                    # print(num_str)
                                                    reflectional += 1
                                                    set_lines.add(line)

                                                    dict_add_pattern([i, i, j, j, i, i])

                                        if find_subarray(arr, [i, i, i, i]):
                                            # print(num_str)
                                            same += 1
                                            set_lines.add(line)

                                            dict_add_pattern([i, i, i, i])

                                        if find_subarray(arr, [j, j, j, j]):
                                            # print(num_str)
                                            same += 1
                                            set_lines.add(line)

                                            dict_add_pattern([j, j, j, j])

                            index += 1

                        # print(translational)
                        # print(reflectional)
                        # print(same)
                        totals.append(sum_all_seq)
                        symmetric.append(len(set_lines))

                        try:
                            proportions.append(round(100*len(set_lines)/sum_all_seq, 2))
                        except ZeroDivisionError:
                            proportions.append(0)
                        
                        # print('total: ', sum_all_seq)
                        # print('symmetric: ', len(set_lines))
                        # print('proportion: ', round(len(set_lines)/sum_all_seq, 2))
                        # print(set_lines)

                print('symmetric all:')
                f_sym.write(f'HR, {setting}\t{lang}\t' + '\t'.join([str(i) for i in symmetric]))
                f_sym.write('\n')
                print('total all:')
                print('\t'.join([str(i) for i in totals]))
                f_total.write(f'HR, {setting}\t{lang}\t' + '\t'.join([str(i) for i in totals]))
                f_total.write('\n')
                print('proportion all:')
                print('\t'.join([str(i) for i in proportions]))
                f_proportions.write(f'HR, {setting}\t{lang}\t' + '\t'.join([str(i) for i in proportions]))
                f_proportions.write('\n')

                for key, value in sorted(patterns_dict.items(), key=lambda x: x[1], reverse=True):
                    real_freq = re.findall(', '.join([str(i) for i in list(key)]), text)
                    # print(key, len(real_freq))
                    f_patterns.write(f'{key} {len(real_freq)}\n')
