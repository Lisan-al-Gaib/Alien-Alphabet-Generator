from PIL import Image
import random
import copy
import os
# SEED LOCK:
random.seed(17051996)

alphabet_size = 3
complexity = 0

alphabet_list = []
tile_list = []

def makeTile(folder):  # for uploading the images to the tile_list
    for file in os.listdir("{}".format(folder)):
        if file[0] == '1':
            tile_list.append({str(file): {

                'flip_h': False,
                'flip_v': False,
                'ports': [True, False],
                'img': "{}/{}".format(folder, file)
            }
            })

        else:
            tile_list.append({str(file): {

                'flip_h': False,
                'flip_v': False,
                'ports': [True, True],
                'img': "{}/{}".format(folder, file)
            }
            })



def testy(folder): # has to be in 
    for files in os.listdir("{}".format(folder)):
        print(files)
#testy('tile_images')

makeTile('tile_images')
for item in tile_list:
    print(item, "\n")