from PIL import Image
import random
import copy

# SEED LOCK:
random.seed(17051996)
# this causes a bug in the 2nd letter.

""" CLARIFICATIONS: """
# tiles: 1/2 a letter 
# letter: mix of 2 tiles. 
# background: canvas for the 2 tiles 
# alphabet: a list of letters 


""" STYLE PARAMETERS: """
alphabet_size = 3  # (26-ish) depends -> incoming number of phonemes.[length of alphabet]
# TBD diff between vowels and consonants in style, or not. separate lists to make...

form = 'square'  # to be expanded (percent for each 4). [2nd layer of listo]
girth = 50  # 0-100. [D or S, 3rd layer of listo]
intricacy = 50  # 0-X. mode of triangulation. Randochoice from list of items in dict. [#, 4th listo]
intr_drift = 60  # 40-100. radius of distance between min & max for POMP

# ================= LISTS ======================

alphabet_list = []

tile_list = {
    'square': {
        'single': {},
        'double': {}
    },

    'round': {
        'single': {},
        'double': {}
    },

    'mixed': {
        'single': {},
        'double': {}
    },

    'pointy': {
        'single': {},
        'double': {}
    }
}


# --------------- FUNCTIONS -------------------

def checkGirth():
    y = random.randrange(0, 100)
    # print('girth_check -->', y)
    if y < girth:
        return 'double'
    else:
        return 'single'


def checkIntricacy(x, y):  # x = form dict, y = D/S dict

    dict_len = len(tile_list.get(x).get(y))  # pulled from getTI() func.

    i_min = intricacy - intr_drift
    i_max = intricacy + intr_drift
    if i_min < 0:
        i_min = 0
    elif i_max > 100:
        i_max = 100

    p = (random.triangular(i_min, i_max, intricacy) / 100)  # rando # 0.0-1.0 from params
    # *** here's the bug!, the triangulation is greater than 1?
    rounded_n = round(dict_len * p)
    if rounded_n > dict_len:
        rounded_n -= 1

    return  str(rounded_n) # returns a number within the length of dict.


def makeTiles(form, port_type, size):  # for uploading the images to the tile_list
    """ thus, you must do this for the doubles and the singles """
    destination = tile_list[form][port_type]
    for item in range(size):
        item += 1  # item now starts at 1
        destination.update({str(item): {

            'flip_h': False,
            'flip_v': False,
            'ports': [True, False],
            'tile_index': item,
            'img': "{}/{}_{}_{}.jpeg".format("tile_images", form[0], port_type[0], item)
        }
        })

        if port_type == 'double':
            destination[str(item)].update({'ports': [True, True]})


def getImage(x, y, z):
    got_img = tile_list.get(x).get(y).get(z).get('img')
    return got_img


def copyTile():  # returns a deep copy a rando tile
    cg_ = checkGirth()
    ci_ = checkIntricacy(form, cg_)
    TI_pick = tile_list.get(form).get(cg_).get(ci_)
    return copy.deepcopy(TI_pick)


def makeLetter():
    """ picks 2 tiles and add as list to AB_list """

    for i in range(alphabet_size):
        LTR_list = []
        for e in range(2):  # Adds two random tiles to LTR_list
            l = copyTile()
            if e:  # if it's the second in the letter list (0:F, 1:T)
                l["flip_v"] = True  # now marked as bottom.
            LTR_list.append(l)

        alphabet_list.append(LTR_list)
        # TBD make sure the second in the list gets flipped upside down!
        # TBD NEXT compare the two tiles and switch them around when need be


# TBD compare all items in the p_r alphabet to each other before image processing:
# - no copies!

# -----------------------------------------------------------------------------------


""" TILE COMPILATION: """
makeTiles('square', 'single', 24)  # singles
makeTiles('square', 'double', 16)  # doubles

# TBD Round
# TBD Mixed
# TBD Pointy


""" IMAGE PROCESSING: """


# get this to pull
def flipH():
    pass


flipH()


def shuffleTiles():
    # open images for letters in x
    # flip images according to data
    # paste onto a lex_root copy
    # save to a new folder

    # DATA Handling
    for letter_i in alphabet_list:  # bottoms already marked as bottoms

        for tile_i in letter_i:

            first = letter_i[0]["ports"]
            second = letter_i[1]["ports"]
            # bot_square = (0, 100, 100, 200)
            # if the first port of the first tile, doesn't match the first port of the second tile, flipH()
            if first[0] != second[0]:
                print("ports don't match!")
            if tile_i["up_top"] == False:  # flips vertically if on bottom
                tile_i["flip_v"] = True
                print("working!")

    # IMAGE Handling!


shuffleTiles()

"""# print(getImage('square', 'double', '1')) # test for getImg
imgo = Image.open(getImage('square', 'double', '1'))  # here is the test image to SHOW!
rooty = Image.open('tile_images/lex_root.jpeg')

lower = (0,100,100,200)
rooty.paste(imgo)
rooty.paste(imgo, lower)
rooty.show()

del rooty
del imgo"""

""" LETTER PRODUCTION: """
makeLetter()

for x in alphabet_list:
    print("LETTER -- ", x, '\n')

print('number of letters in AB:', len(alphabet_list))
