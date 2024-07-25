import myutils
import os


for strict in [True, False]:
    tgt_dir = 'symmetry_proportions'
    if strict:
        tgt_dir += '_strict'
    else:
        tgt_dir += '_notstrict'
    
    
    # TODO this is very redundant with the "random" code below
    data_dir = 'segmentations_data/'
    for dataset in myutils.datasets:
        out_dir = os.path.join(tgt_dir, dataset)
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        out_file = open(os.path.join(out_dir, 'symmetric.txt'), 'w')
        print(os.path.join(out_dir, 'symmetric.txt'))
        
        for setting in myutils.settings:
            setting_path = os.path.join(data_dir, dataset, setting)
            if not os.path.isdir(setting_path):
                continue
    
            for lang_file in os.listdir(setting_path):
                if not lang_file.endswith('_results.csv'):
                    continue
                
                lang = lang_file.split('_')[0]
                segments = [eval(x.split('\t')[1]) for x in open(setting_path + '/' + lang_file).readlines()[1:]]
                buckets = [[0,0], [0,0], [0,0], [0,0], [0,0]]
                totalcounts = [0,0]
                for word_parts in segments:
                    symmetric = myutils.is_symmetric(word_parts, strict)
                    if symmetric == None:
                        continue
                    totalcounts[int(symmetric)] += 1
                    length = sum(word_parts)
                    if length < 5:
                        buckets[0][int(symmetric)] += 1
                    elif length < 9:
                        buckets[1][int(symmetric)] += 1
                    elif length < 13:
                        buckets[2][int(symmetric)] += 1
                    elif length < 17:
                        buckets[3][int(symmetric)] += 1
                    else:
                        buckets[4][int(symmetric)] += 1
                buckets = ['--' if x+y < 3 else y/(x+y) for x, y in buckets]
                data = [dataset, setting, lang, 1,totalcounts[1]/sum(totalcounts)] + buckets
                data = [str(x) for x in data]
                out_file.write('\t'.join(data) + '\n')
        out_file.close()
    
    
    
    data_dir = 'random_baselines'
    
    for dataset in myutils.datasets:
        out_dir = os.path.join(tgt_dir, dataset)
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
    
        out_file = open(os.path.join(out_dir, 'symmetric_baselines.txt'), 'w')
        print(os.path.join(out_dir, 'symmetric_baselines.txt'))
        for seed in myutils.seeds:
            for setting in myutils.settings:
                in_dir = os.path.join(data_dir, dataset, '5_random_seeds', str(seed), setting)
                if not os.path.isdir(in_dir):
                    continue
        
                for lang_file in os.listdir(in_dir):
                    if not lang_file.endswith('_baseline.csv'):
                        continue
                    lang = lang_file.split('_')[0]
                    segments = [eval(x.split('\t')[1]) for x in open(in_dir + '/' + lang_file).readlines()[1:]]
    
                    buckets = [[0,0], [0,0], [0,0], [0,0]]
                    totalcounts = [0,0]
                    for word_parts in segments:
                        symmetric = myutils.is_symmetric(word_parts, strict)
                        if symmetric == None:
                            continue
                        totalcounts[int(symmetric)] += 1
                        length = sum(word_parts)
                        if length < 4:
                            continue
                        elif length < 8:
                            buckets[0][int(symmetric)] += 1
                        elif length < 12:
                            buckets[1][int(symmetric)] += 1
                        elif length < 16:
                            buckets[2][int(symmetric)] += 1
                        else:
                            buckets[3][int(symmetric)] += 1
                    buckets = ['--' if x+y < 3 else y/(x+y) for x, y in buckets]
                    data = [dataset, setting, lang, str(seed), totalcounts[1]/sum(totalcounts)] + buckets
                    data = [str(x) for x in data]
                    out_file.write('\t'.join(data) + '\n')
                    
        out_file.close()
