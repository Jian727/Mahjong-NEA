from itertools import combinations, chain
from collections import Counter

'''def contains_all_elements_with_duplicates(array1, array2):
    counter_array1 = Counter(array1)
    counter_array2 = Counter(array2)

    return all(count <= counter_array1[key] for key, count in counter_array2.items())


deck = [0,0,0,1,2,3,4,5,6,31,31,31,32,32]
dot = [0,0,0,1,2,3,4,5,6]
bamboo = []
char = []
wind = []
dragon = [31,31,31,32,32]
set_of_three = [dot, bamboo, char, wind, dragon]
x=[]
comb_of_three = []
winning_deck_comb =[]


for group in set_of_three:

    if len(group)>=3:
        x.append(group)



for group in x:

    for comb in combinations(group, 3): 
        comb = sorted(comb)
        pung = all(elem == comb[0] for elem in comb)
        chow = (comb == list(range(comb[0], comb[-1] + 1)))

        if pung or chow:
            comb_of_three.append(comb)



if len(comb_of_three) < 4:
    print([])
else:
    for full_comb in combinations(comb_of_three, 4):
        joined = list(chain.from_iterable(full_comb))
        if contains_all_elements_with_duplicates(deck, joined): #wrong
            pair  = [elem for elem in deck if elem not in joined]
            if pair[0] == pair[1] and len(pair) == 2:
                temp = list(full_comb)
                temp.append(pair)
                winning_deck_comb.append(temp)
    print (winning_deck_comb)'''

array = range(34)
for i in array:
    print (f"value: {i}, {i%3}")