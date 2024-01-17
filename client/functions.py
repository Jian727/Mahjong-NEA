from collections import Counter
from tiles import *

def checksubset(array1, array2): #if array2 a subset array1
    counter_array1 = Counter(array1)
    counter_array2 = Counter(array2)
    return all(count <= counter_array1[key] for key, count in counter_array2.items())


def checkPung(tiles):
    return all(elem.get_cal_value() == tiles[0].get_cal_value() for elem in tiles)

def checkChow(tiles): #check attribute in same suit
    for i in tiles:
        if isinstance(i, Honor):
            return False
    tile1, tile2, tile3 = tiles
    if tile1.get_type() == tile2.get_type() == tile3.get_type():
        values = [obj.get_cal_value() for obj in tiles]
        values.sort()
        return (values == list(range(values[0], values[-1] + 1)))
    return False

def checkSameTileInArray(tile, array):
    for i in array:
        if all(getattr(tile, attr) == getattr(i, attr) for attr in vars(tile)):
            return True
    return False

#functions for testing only

def tilesToNum(tiles):
    result =[]
    
    for tile in tiles:
        if type(tile) is list:
            temp_result=[]
            for i in tile:
                temp_result.append(i.get_cal_value())
            result.append(temp_result)
        else:
            result.append(tile.get_cal_value())
    return result

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


