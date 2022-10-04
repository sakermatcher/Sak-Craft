import pygame, sys
import os
import importlib

os.chdir(os.path.normpath(os.getcwd() + os.sep + os.pardir))

pygame.init()

size = width, height = 1000, 1000
selectedBlockXZY = [0,0,0]
structureDims = [5,10,9]#X, Z, Y
matrix = []
rester = 0
mother = [0,0,0]

oofsetX, oofsetZ = 0, 0
black = 10, 100, 10

screen = pygame.display.set_mode(size)
events = pygame.event.get()
screen.fill(black)

packs= ['vanilla']

blocks= []
textures= {}

for pack in packs:
    for thing in importlib.import_module('packs.'+pack+'.manifest').manifest["stuff"]["blocks"].keys():
        blocks.append (importlib.import_module('packs.'+pack+'.manifest').manifest["stuff"]["blocks"][thing])
    for thing in importlib.import_module('packs.'+pack+'.manifest').manifest["stuff"]["textures"].keys():
        textures[thing] = importlib.import_module('packs.'+pack+'.manifest').manifest["stuff"]["textures"][thing]
    
defaultSelect = pygame.image.load("helpers/textures/select.png").convert_alpha()

def cutLR(LR):
    out = False
    for k in range(len(matrix[0][0])):
        for i in range (len(matrix)):
            for l in range (len(matrix[i])):
                if matrix[i][l][LR]['id'] not in ['vanilla:air','vanilla:visual']:
                    out = True
                    break
            if out:
                break
        if out:
            break
 
    if not out:
        for i in range (len(matrix)):
            for l in range (len(matrix[i])):
                del matrix[i][l][LR]
        cutLR(LR)

def cutUD(UD):
    out = False
    for k in range (len(matrix)):
        for l in range (len(matrix[UD][0])):

            if matrix[k][UD][l]['id'] not in ['vanilla:air','vanilla:visual']:
                out = True
                break
            
        if out:
            break
 
    if not out:
        for i in range (len(matrix)):
            del matrix[i][UD]
        cutUD(UD)

for y in range(structureDims[2]):
    matrix.append([])
    for z in range(structureDims[1]):
        matrix[y].append([])
        for x in range(structureDims[0]):
            if y == 0:
                matrix[y][z].append({'id':'devVisual',  'name':'air'})

            elif x == 0 and z == 0 and y == structureDims[2] - 1:
                matrix[y][z].append({'id':'vanilla:free'})

            elif x == 0 and z == 0:
                matrix[y][z].append({'id':'vanilla:visual',  'name':'air'})

            else:
                matrix[y][z].append({'id':'vanilla:air',  'name':'air'})

originalFrame = pygame.image.load("helpers/textures/frame.png").convert_alpha()
originalSurf = pygame.image.load("helper/bak.png").convert_alpha()
pygame.transform.scale(originalSurf, (structureDims[0]*100,structureDims[1]*50))
surf = originalSurf.copy()

#setup your selected block (default: grass)
selected= 0
selectedBlock = blocks.values()[selected]

def generate():
    screen.fill(black)
    surf = originalSurf.copy()

    #check if you go outside the selected dimentions
    if selectedBlockXZY[0] not in range(len(matrix[0][0])):
        selectedBlockXZY[0] = int(len(matrix[0][0])/2)

    elif selectedBlockXZY[1] not in range(len(matrix[0])):
        selectedBlockXZY[1] = int(len(matrix[0])/2)

    elif selectedBlockXZY[2] not in range(len(matrix)+rester):
        selectedBlockXZY[2] = int((len(matrix)+rester)/2)

    for y in range(len(matrix)+rester):
        for z in range(len(matrix[y])):
            for x in range(len(matrix[y][z])):

                if selectedBlockXZY == [x, z, y]:

                        if z%2 == 0: 
                        
                            pygame.Surface.blit(surf, defaultSelect, dest=(x*100, z*40 - y*30 + structureDims[2]*30))

                        else:
                        
                            pygame.Surface.blit(surf, defaultSelect, dest=(x*100+50, z*40- y*30 + structureDims[2]*30))
                else:

                    if matrix[y][z][x]['id'] != 'vanilla:air':

                        if z%2 == 0: 

                            pygame.Surface.blit(surf, textures[blocks[matrix[y][z][x]].args['id']], dest=(x*100, z*40 - y*30 + structureDims[2]*30))

                        else:

                            pygame.Surface.blit(surf, textures[[y][z][x].texture], dest=(x*100+50, z*40- y*30 + structureDims[2]*30))

    screen.blit(surf, dest=(oofsetX,oofsetZ))
    screen.blit(originalFrame, dest=(0,0))
    screen.blit(blocks[selectedBlock['id']], dest=(10,10))
    pygame.display.flip()
    

generate()


while 1:

    events = pygame.event.get()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()

    keys = list(pygame.key.get_pressed())

    if True:
        
        if keys[pygame.KSCAN_1] == 1:
            selectedBlock = {'id':list(blocks.keys())[0],  'name':blocks[list(blocks.values()][0]())[0]], 'state':''}

        elif keys[pygame.KSCAN_2] == 1:
            selectedBlock = {'id':list(blocks.keys())[1],  'name':namePerID[list(pallete.keys())[1]], 'state':''}

        elif keys[pygame.KSCAN_W] == 1:
            selectedBlockXZY[1] -= 1
            

        elif keys[pygame.KSCAN_D] == 1:
            selectedBlockXZY[0] += 1
            

        elif keys[pygame.KSCAN_S] == 1:
            selectedBlockXZY[1] += 1
            

        elif keys[pygame.KSCAN_A] == 1:
            selectedBlockXZY[0] -= 1
            


        elif keys[pygame.KSCAN_UP] == 1:
            oofsetZ += 50
            

        elif keys[pygame.KSCAN_RIGHT] == 1:
            oofsetX -= 50
            

        elif keys[pygame.KSCAN_DOWN] == 1:
            oofsetZ -= 50
            

        elif keys[pygame.KSCAN_LEFT] == 1:
            oofsetX += 50
            

        elif keys[pygame.KSCAN_Q] == 1:
            selectedBlockXZY[2] -= 1
            

        elif keys[pygame.KSCAN_E] == 1:
            selectedBlockXZY[2] += 1

        elif keys[pygame.KSCAN_LCTRL] == 1:
            rester -= 1 

        elif keys[pygame.KSCAN_LSHIFT] == 1:
            rester += 1

        elif keys[pygame.KSCAN_BACKSPACE] == 1:
            matrix[selectedBlockXZY[2]][selectedBlockXZY[1]][selectedBlockXZY[0]] = {'id':'defaultAir',  'name':'air', 'state':''}

        elif keys[pygame.KSCAN_SPACE] == 1:
            matrix[selectedBlockXZY[2]][selectedBlockXZY[1]][selectedBlockXZY[0]] = selectedBlock.copy()

        elif keys[pygame.KSCAN_L] == 1:
            #from newStructure import model
            from grassTree import model
            matrix = model


        elif keys[pygame.KSCAN_G] == 1:

            cutLR(0)

            cutLR(-1)

            cutUD(0)

            cutUD(-1)

            opnr = open('newStructure.py', 'w+')
            opnr.write ('mother = ' + str(mother) + '\n\nmodel = ' + str(matrix).replace('devVisual', 'defaultAir'))
            opnr.close

        elif keys[pygame.KSCAN_M] == 1:
            mother = selectedBlockXZY

        generate()

        while 1 in list(pygame.key.get_pressed()):
            events = pygame.event.get()