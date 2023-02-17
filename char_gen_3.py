import os, copy, pprint, random
from PIL import Image

#random.seed(19960517)

# ADD A 'NONE' value if you want it to be random!

#=====================================================================

desired_length = 30 # HOW MANY?
variety = 100 # HOW DIFFERENT?
form = 100  # HOW CHUNKY?
culture = 5 # HOW COMPLEX MACRO?
#gusto = 50 # HOW COMPLEX MIRCO?
clones = 0 # HOW MANY SIMILIAR LETTERS?

folder_name = "example_4"

#=====================================================================

def getSelection(d): # returns the amount to select for 
    counter = 0 
    for x in range(d):
        if x*(x+1) < d:
            counter += 1
        else:
            return counter+1
            break

if not variety: # if zero
    select_amount = getSelection(desired_length)
else:
    select_amount = getSelection( round(desired_length * ((variety/100)+1)) )

selections = []
old_tile_list = {
    1: {
        1: {},
        2: {},
        3: {},
    },
    2: {
        1: {},
        2: {},
        3: {},
    }}

def importTiles():
    for item in os.listdir("tile_images"):
        port, group = int(item[0]), int(item[2])
        # this is for double digit bugs in TILE
        try:
            int(item[4:-4])
        except ValueError:
            tile = int(item[4])
        else:
            tile = int(item[4:-4])
        outbound = old_tile_list[port][group]
        
        outbound.update({tile: {
            'clone': False, # flip vertical
            'img': item # image
            }})
        

tile_list = {}

# this sucker sorts a triple nested dictionary. eat yer heart out!
def sortTiles():
    for port in old_tile_list:
        tile_list.update({port:{}})
        for group in old_tile_list[port]:
            tile_list[port].update({group:{}})
            y = old_tile_list[port][group]
            x = sorted(y.keys())
            tile_list[port][group].update({key:y[key] for key in x})
        

importTiles()
sortTiles()

#NOW WE HAVE AN ORDERED DICTIONARY/LIST OF ALL TILES

#______________________________________________________________________________
#______________________________________________________________________________

def selectTile(): # merged select and copy
    # FORM
    F = 2 if random.randrange(0, 100) < form else 1
    # CULTURE
    C = round(random.triangular(0, 100, culture) // 33.333) + 1
    # GUSTO
    G = max(1,(round(len(tile_list[F][C])*(min(1,random.randint(1, 100)/100)))) )

    pick = tile_list.get(F).get(C).get(G)
    return copy.deepcopy(pick)


def addSelections(a):
    counter = 0
    s = []
    while len(s) < a:
        t = selectTile()
        if t not in s:
            s.append(t)
        else:
            counter +=1
    else:
        return s

def permy(iterable):
    # probably trim this down to size!
    pool = list(iterable)
    n = len(pool)
    r = 2
    if r > n:
        return
    indices = list(range(n)) # i
    cycles = list(range(n,n-r, -1))
    
    yield list(copy.deepcopy(pool[i]) for i in indices[:r])
    ########################
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield list(copy.deepcopy(pool[i]) for i in indices[:r])
                break
        else:
            return
        
select_perms = list(permy(addSelections(select_amount)))

random.shuffle(select_perms)

final_perms = select_perms[0:desired_length]

#==================================================
#==================================================

def getImage(x):
    img = "tile_images/{}".format(x)
    return img


bot_coord = (0,7,7,14) # base image is 7x14 px

def makeLetterImages():
    name = folder_name #.format(random.randint(1000,9999))
    current_dir = os.getcwd()
    new_path = os.path.join(current_dir,name)

    if not os.path.exists(new_path):
        os.makedirs(new_path)
    else:
        print("Folder already exists ya dummy!")

    counter = 1
    for letter in final_perms:
        base = Image.open('bg_image.png') 
        top_img = Image.open(getImage(letter[0]['img']))
        bot_img = Image.open(getImage(letter[1]['img'])) # 0=H 1=V
        k = 1 if random.randrange(0,100) < clones else 0
        if k:
            #flips if clones
            base.paste(top_img.transpose(method=0))
            base.paste(bot_img.transpose(method=0).transpose(method=1), bot_coord)
        else:
            base.paste(top_img)
            base.paste(bot_img.transpose(method=1), bot_coord)

        base.save("{}/l_{}.png".format(name, str(counter)))

        top_img.close()
        bot_img.close()
        base.close()
        counter +=1

makeLetterImages()