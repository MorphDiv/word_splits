import myutils
import os

def compositions(n):
    def backtrack(curr_composition, remaining):
        if remaining == 0:
            result.append(curr_composition[:])
            return
        for i in range(1, remaining + 1):
            curr_composition.append(i)
            backtrack(curr_composition, remaining - i)
            curr_composition.pop()

    result = []
    backtrack([], n)
    return result


max_len = 24

for strict in [True, False]:
    lookup = {}
    for size in range(max_len+1):
        comps = compositions(size)
        total = 0
        symmetric = 0
        for composition in comps:
            is_symmetric = myutils.is_symmetric(composition, strict)
            if is_symmetric == True: # TO skip the None
                symmetric+=1
            if is_symmetric in [True, False]:
                total += 1
        if total == 0:
            lookup[size] = 0.0
        else:
            lookup[size] = symmetric/total
    print(lookup)
        
    tgt_dir = 'symmetry_proportions'
    if strict:
        tgt_dir += '_strict'
    else:
        tgt_dir += '_notstrict'
    
    data_dir = 'segmentations_data/'
    for dataset in myutils.datasets:
        out_dir = os.path.join(tgt_dir, dataset)
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        out_file = open(os.path.join(out_dir, 'expected.txt'), 'w')
        print(os.path.join(out_dir, 'expected.txt'))
        setting = os.listdir(os.path.join(data_dir, dataset))[0]
        setting_path = os.path.join(data_dir, dataset, setting)
        for lang_file in os.listdir(setting_path):
            if not lang_file.endswith('_results.csv'):
                continue
            print('\t' + lang_file)
            lang = lang_file.split('_')[0]
            lengths = [int(x.split('\t')[2]) for x in open(setting_path + '/' + lang_file).readlines()[1:]]

            buckets = [[], [], [], []]
            for word_length in lengths:
                if word_length in lookup:
                    expectation = lookup[word_length]
                else:
                    expectation = lookup[max_len]

                if word_length < 4:
                    continue
                elif word_length < 8:
                    buckets[0].append(expectation)
                elif word_length < 12:
                    buckets[1].append(expectation)
                elif word_length < 16:
                    buckets[2].append(expectation)
                else:
                    buckets[3].append(expectation)
            for bucketIdx, bucket in enumerate(buckets):
                out_file.write('\t'.join([lang, str(bucketIdx), str(bucket)]) + '\n')
        out_file.close()
    
    
    
