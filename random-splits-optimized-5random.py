import numpy as np
import os

seed_num = 5
np.random.seed(seed_num)


def insert_split(string, i):
    return string[:i] + '|' + string[i:]


def find_all(s, character):
    res = []
    idx = s.find(character)
    while idx != -1:
        res.append(idx)
        idx = s.find(character, idx + 1)
    return res


settings = ['manual', 'spm', 'wordpiece',
            'bpe-mr', 'bpe04V', 'morf']

for setting in settings:
    for root, dirs, files in os.walk('../data/aalto/' + setting):
        for file in files:
            if '_results' in file and ('eng' in file or 'fin' in file or 'tur' in file):
                print(file)
                with open(os.path.join(root, file), 'r') as f:
                    num_splits = 0
                    long_line = ''
                    for line in f:
                        if 'word_split' not in line and '|	[0, 0]	0	0	0' not in line:
                            word_splits = line.split('\t')[0]
                            long_line += word_splits.replace('|', '') + '\n'
                            for char in word_splits:
                                if char == '|':
                                    num_splits += 1

                    long_line = long_line.strip()
                    delim = find_all(long_line, '\n')
                    valid_ids = set(range(len(long_line) - 1)) - (set(delim) | set([i - 1 for i in delim]))

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

                    #setting = setting.replace('gold-list/', '')

                    if not os.path.exists(f'./{seed_num}/{setting}'):
                        os.mkdir(f'./{seed_num}/{setting}')

                    with open(f'./{seed_num}/{setting}/' + file.replace('_results', '_baseline'),
                              'w') as f_result:
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
