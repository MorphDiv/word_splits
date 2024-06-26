settings = ['manual', 'spm', 'wordpiece',
            'bpe-mr', 'bpe04V', 'morf']
datasets = ['aalto_3lang', 'hr_19lang', 'lr_13lang']
seeds = [1,2,3,4,5]

# 1,3,2 = reflectional + translational? it is caught in the second part here
def is_translational_symmetric(composition):
    # First test is there is a reccuring n-gram:
    for size in range(1,int(len(composition)/2+1)):
        if len(composition)%size == 0:
            splits = []
            # make same sized splits
            for split in range(0, len(composition), size):
                splits.append('-'.join([str(x) for x in composition[split:split+size]]))
            # If they are all the same, return True
            if len(set(splits)) == 1:
                return True

    # We introduce a split in the middle by creating a first
    # and last chunk. The middle subword will be included in both
    # This should catch cases like 1,3,2 and 2,3,1 (which are 1,2,1,2 after 
    # the new split
    #middle = int(sum(composition)/2)
    #cur = 0
    #for posIdx, length in enumerate(composition):
    #    cur += length
    #    if cur == middle:
    #        first = composition[:posIdx]
    #        last = composition[posIdx:]
    #        break
    #    if cur > middle:
    #        first = composition[:posIdx] + [middle-(cur-length)]
    #        last = [cur - middle] + composition[posIdx+1:]
    #        break
    #return first == last
    return False

def is_reflectional_symmetric(composition):
    return composition == list(reversed(composition))


def is_symmetric(composition):
    return is_reflectional_symmetric(composition) or is_translational_symmetric(composition)
