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

# Example usage:
number = 4
all_compositions = compositions(number)


def is_translational_symmetric(composition):
    n = len(composition)
    for i in range(1, n):
        if composition[i:] + composition[:i] == composition:
            return True
    # What about the one below for odd lengths?
    middle = int(sum(composition)/2)
    cur = 0
    for posIdx, length in enumerate(composition):
        cur += length
        if cur == middle:
            first = composition[:posIdx]
            last = composition[posIdx:]
            break
        if cur > middle:
            first = composition[:posIdx] + [middle-(cur-length)]
            last = [cur - middle] + composition[posIdx+1:]
            break
    return first == last

def is_reflectional_symmetric(composition):
    if len(composition)%2 == 1:
        split = int(len(composition)/2)
        composition = composition[:split] + composition[split+1:]
    return composition == composition[::-1]
print('number', 'numCompositions', 'trans', 'reflect', 'total')

# Example usage:
for number in range(1,20):
    is_trans = 0
    is_reflect = 0
    is_sym = 0
    all_compositions = compositions(number)
    for composition in all_compositions:
        #print("Composition:", composition)
        #print("Translational Symmetry:", is_translational_symmetric(composition))
        #print("Reflectional Symmetry:", is_reflectional_symmetric(composition))
        #print()
        if is_translational_symmetric(composition):
            is_trans += 1
            #if number == 8:
            #    print(composition)

        if is_reflectional_symmetric(composition):
            is_reflect += 1
        if is_reflectional_symmetric(composition) or is_translational_symmetric(composition):
            #if number == 6:
            #    print(composition)
            is_sym += 1

    #print(number, is_trans, is_reflect, is_sym)
    if number%2 == 0:
        print(number, len(all_compositions), is_trans, is_reflect, is_sym)

