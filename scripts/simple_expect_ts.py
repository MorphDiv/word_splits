import myutils


for strict in [True, False]:           # dummy function, just to have the name "strict" defined
    tgt_dir = 'symmetry_proportions'
    if strict:
        tgt_dir += '_strict'
    else:
        tgt_dir += '_notstrict'
    


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


for size in range(3,21):
    symmetric = 0
    comps = compositions(size)
    total = len(comps)-2
    print("Length", size)
    for item in comps:
        is_symmetric = myutils.is_symmetric(item, strict)
#        print(item,is_symmetric)   #for checking
        if is_symmetric == True: # TO skip the None
            symmetric+=1
    print("Symmetric",symmetric-2)
    print("Total", total)
    print((symmetric-2)/total, "\n")


