import numpy as np
import os
import myutils



def insert_split(string, i):
    return string[:i] + '|' + string[i:]


def find_all(s, character):
    res = []
    idx = s.find(character)
    while idx != -1:
        res.append(idx)
        idx = s.find(character, idx + 1)
    return res

def gen_random_results(out_path, lang_file, seed, long_line, delim, valid_ids, num_splits):
    out_file = os.path.join(out_path, lang_file.replace('_results.csv', '_baseline.csv'))
    print(out_file)
    if os.path.isfile(out_file):
        return
    np.random.seed(seed)
    random_indeces = np.random.choice(list(valid_ids), num_splits, replace=False)
    random_indeces = sorted(random_indeces)
    random_indeces = [random_indeces[j] + j for j in range(len(random_indeces))]

    new_array = [''] * (len(long_line) + len(random_indeces))

    for i in random_indeces:
        new_array[i + 1] = '|'

    empty_positions = [i for i in range(len(new_array)) if new_array[i] != '|']

    for i in range(len(long_line)):
        j = empty_positions[i]
        c = long_line[i]
        new_array[j] = c

    result = ''.join(new_array)

    if not os.path.exists(out_path):
        os.mkdirs(out_path)

    with open(out_file, 'w') as f_result:
        f_result.write('word_split\tsegments_lengths\tword_length\tindex\n')
        long_line_arr = long_line.split('\n')

        # sanity check
        if '\n|' in result or '|\n' in result or '||' in result:
            print('EXCEPTION')

        for word in result.split('\n'):
            splits = [len(split) for split in word.split('|')]
            word_length = len(word.replace('|', ''))
            index = max(splits) - min(splits)
            f_result.write(f'{word}\t{splits}\t{word_length}\t{index}\n')

data_dir = 'segmentations_data/'
for dataset in myutils.datasets:
    for setting in myutils.settings:
        setting_path = os.path.join(data_dir, dataset, setting)
        if not os.path.isdir(setting_path):
            continue
        print(setting_path)
        for lang_file in os.listdir(setting_path):
            if not lang_file.endswith('_results.csv'):
                continue
            lang_path = os.path.join(data_dir, dataset, setting, lang_file)
            num_splits = 0
            long_line = ''
            for line in open(lang_path):
                if 'word_split' not in line and '|	[0, 0]	0	0	0' not in line:
                    word_splits = line.split('\t')[0]
                    long_line += word_splits.replace('|', '') + '\n'
                    for char in word_splits:
                        if char == '|':
                            num_splits += 1

            long_line = long_line.strip()
            delim = find_all(long_line, '\n')
            valid_ids = set(range(len(long_line) - 1)) - (set(delim) | set([i - 1 for i in delim]))
            for seed in myutils.seeds:
                out_path = os.path.join('random_baselines', dataset, '5_random_seeds', str(seed), setting)
                gen_random_results(out_path, lang_file, seed, long_line, delim, valid_ids, num_splits)


