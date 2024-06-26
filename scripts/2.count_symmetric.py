import myutils
import os

tgt_dir = 'symmetry_proportions2'

data_dir = 'segmentations_data/'
for dataset in myutils.datasets:
    continue
    out_dir = os.path.join(tgt_dir, dataset)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    out_file = open(os.path.join(out_dir, 'symmetric.txt'), 'w')
    for setting in myutils.settings:
        setting_path = os.path.join(data_dir, dataset, setting)
        if not os.path.isdir(setting_path):
            continue

        for lang_file in os.listdir(setting_path):
            if not lang_file.endswith('_results.csv'):
                continue
            
            lang = lang_file.split('_')[0]
            segments = [eval(x.split('\t')[1]) for x in open(setting_path + '/' + lang_file).readlines()[1:]]
            results = [myutils.is_symmetric(segment) for segment in segments]
            print(setting_path +'/'+ lang_file, len(results), sum(results), sum(results)/len(results))
            sym_ratio = sum(results)/len(results)
            data = [dataset, setting, lang, len(results), sum(results), sym_ratio]
            data = [str(x) for x in data]
            out_file.write('\t'.join(data) + '\n')
    out_file.close()



data_dir = 'random_baselines'

for dataset in myutils.datasets:
    out_dir = os.path.join(tgt_dir, dataset)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    out_file = open(os.path.join(out_dir, 'symmetric_baselines.txt'), 'w')
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
                results = [myutils.is_symmetric(segment) for segment in segments]
                print(in_dir +'/'+ lang_file, len(results), sum(results), sum(results)/len(results), seed)
                sym_ratio = sum(results)/len(results)
                data = [dataset, setting, lang, len(results), sum(results), sym_ratio, str(seed)]
                data = [str(x) for x in data]
                out_file.write('\t'.join(data) + '\n')
                
    out_file.close()
