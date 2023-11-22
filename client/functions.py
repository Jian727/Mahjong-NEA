from collections import Counter
from tiles import *

def checksubset(array1, array2): #if array2 a subset array1
    counter_array1 = Counter(array1)
    counter_array2 = Counter(array2)
    return all(count <= counter_array1[key] for key, count in counter_array2.items())

def remove_tiles(deck, tiles):
    return [x for x in tiles if x not in deck]

def checkPung(tiles):
    return all(elem.get_cal_value() == tiles[0].get_cal_value() for elem in tiles)

def checkChow(tiles):
    values = [obj.get_cal_value() for obj in tiles]
    return (values == list(range(values[0], values[-1] + 1)))

def checkSameTileInArray(tile, array):
    for i in array:
        if all(getattr(tile, attr) == getattr(i, attr) for attr in vars(tile)):
            return True
    return False

#functions for testing only

def tilesToNum(tiles):
    return [obj.get_cal_value() for obj in tiles]

def numToTiles(num):
    result = []
    for i in num:
        if i < 27:
            type = i//9 * 9
        elif i < 31:
            type = 27
        else:
            type = 31
        value = i-type
        result.append(Tiles(type, value))
    return result
