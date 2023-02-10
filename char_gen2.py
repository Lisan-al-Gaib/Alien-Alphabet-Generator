import os, copy, pprint, random

#random.seed(199605171800)

alphabet_length = 3
alphabet_list = []

form = 50  # PORT. which way does it lean?0-100
culture = 50 # GROUP. should have deviation 
gusto = 50 # TILE. wider distribution & deviation


# 6, 10, 10 --- 5, 7, 18
tile_list = {
    '1': {
        '1': {},
        '2': {},
        '3': {}
    },

    '2': {
        '1': {},
        '2': {},
        '3': {},
    }
}

""" THIS SHOULD SORT() THE TILES IN GROUPS BY THEIR KEY"""
def importTiles():
	for item in os.listdir("tile_images"):
		port, group = item[0], item[2]
		# this is for double digit bugs in TILE
		if item[5] == ".":
			tile = item[4] 
		else:
			tile = item[4] + item[5]

		outbound = tile_list[port][group]

		outbound.update({str(tile): {
			'flip_HV': [False, False],
            'ports': [True, False],
            'img': item
			}})

		

importTiles()
#priti = pprint.pprint(tile_list)
#print(priti)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def getForm():
    if random.randrange(0, 100) < form:
        return '2'
    else:
        return '1'

def getCulture():
	c = random.triangular(0, 100, culture)//33.333
	C = round(c)+1
	return C
	#print(C)


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def randoCopyTile():  # returns a deep copy a rando tile
    #r_form = 
    #r_culture = 
    #r_gusto = 
    #return copy.deepcopy(pick)
    pass


def makeLetter():
    """ picks 2 tiles and add as list """

    for i in range(alphabet_length):
        letter_list = []
        for item in range(2):  # Adds two random tiles to LTR_list
            selection = randoCopyTile()
            if item:  # if it's the second in the letter list (0:F, 1:T)
                selection["flip_HV"][1] = True  # now marked as bottom.
            letter_list.append(selection)

        alphabet_list.append(letter_list)


# things we need:
# COMPLEXITY = 1.FORM(ports), 2.CULTURE(group), 3.GUSTO(tile)
for i in range(100):
	getCulture()

def getGusto():
	x = getForm()
	y = getCulture()
	#print(tile_list)
	dict_len = tile_list.get(x).get(y)
	print(dict_len)
   
getGusto()