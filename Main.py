#$imports

import json
import sys, pygame
from helpers.construct import pearl
import math
import PySimpleGUI as sg
import importlib

#@imports

pygame.init()

#$variables

opnr = ''
worldName = 'wrld'
size = width, height = 1000, 800
black = 10, 100, 10
oofsetZ = 600
oofsetX = 600
walkAnim = True
chunkDimX = 12
chunkDimZ = 24
chunkDimY = 5
pstChunkX = 1000
pstChunkZ = 1000
oofsetXR = 600
oofsetZR = 600
packs= ['vanilla']
nameTag= 'Sakermatcher'
blocks={}
items={}
textures={}
generation= {}
players= {}
loadedWorld= {'d0':{}}
screen = pygame.display.set_mode(size)
events = pygame.event.get()

with open ('worlds/'+worldName+'.json') as opnr:
    world= json.load(opnr)

for pack in packs:
    for thing in importlib.import_module('packs.'+pack+'.manifest').manifest["stuff"]["blocks"].keys():
        blocks[thing] = importlib.import_module('packs.'+pack+'.manifest').manifest["stuff"]["blocks"][thing]
    for thing in importlib.import_module('packs.'+pack+'.manifest').manifest["stuff"]["items"].keys():
        items[thing] = importlib.import_module('packs.'+pack+'.manifest').manifest["stuff"]["items"][thing]
    for thing in importlib.import_module('packs.'+pack+'.manifest').manifest["stuff"]["textures"].keys():
        textures[thing] = importlib.import_module('packs.'+pack+'.manifest').manifest["stuff"]["textures"][thing]
    for thing in importlib.import_module('packs.'+pack+'.manifest').manifest["stuff"]["generation"].keys():
        generation[thing] = importlib.import_module('packs.'+pack+'.manifest').manifest["stuff"]["generation"][thing]

#@variables

#$IDs

defaultSteveR = pygame.image.load("engine/player/steveR.png")
defaultSteveL = pygame.image.load("engine/player/steveL.png")
surf = pygame.image.load("engine/bak.png").convert_alpha()

#@IDs


#$character

steveLrect = defaultSteveL.get_rect().move(450, 350)
steveRrect = defaultSteveR.get_rect().move(450, 350)

#@character

#$functions

def render(type):
#$funcRender
    global worldName, oofsetX, oofsetZ, surf, wrld, loadedWorld, oofsetXR, oofsetZR
    first = False

    if type == 'walk':
        urX = math.floor(oofsetX/100)
        urZ = math.floor(oofsetZ/50)
        urChunkX = math.ceil(urX/chunkDimX)
        urChunkZ = math.ceil(urZ/chunkDimZ)

        if f'{urChunkZ}_{urChunkX}' not in loadedWorld['d0'].keys():
            loadedWorld= {}
            chunkChange('d0', urChunkX, urChunkZ)
            oofsetXR = 100+(urX - urChunkX *chunkDimX)*100
            oofsetZR = 100+(urZ - urChunkZ *chunkDimZ)*50
            first= True

        if first == True:
            for y in range(chunkDimY):
                for z in range(chunkDimZ):
                    for x in range(chunkDimX):
                        if z%2 == 0 and textures[loadedWorld["d0"][f'{urChunkZ}_{urChunkX}'][y][z][x].texture] != None: 
                                
                            pygame.Surface.blit(surf, textures[loadedWorld["d0"][f'{urChunkZ}_{urChunkX}'][y][z][x].texture], dest=(x*100+500, z*40 - y*30 + 500))

                            
                        elif textures[loadedWorld["d0"][f'{urChunkZ}_{urChunkX}'][y][z][x].texture] != None:
                                
                            pygame.Surface.blit(surf, textures[loadedWorld["d0"][f'{urChunkZ}_{urChunkX}'][y][z][x].texture], dest=(x*100+550, z*40 - y*30 + 500))

        screen.fill(black)
        screen.blit(surf, dest=(-1000 - oofsetXR, -1000 - oofsetZR))
        if walkAnim == True:
            screen.blit(defaultSteveL, steveLrect)
        else:
            screen.blit(defaultSteveR, steveRrect)

        pygame.display.flip()
#@funcRender

def chunkChange(dimention, urX, urZ):
#$funcChunkChange

    if dimention not in loadedWorld.keys():
        loadedWorld[dimention] = {}

    if f'{urZ}_{urX}' not in world['world'][dimention].keys():
        generate= generator(urX, urZ)
        loadedWorld[dimention][f'{urZ}_{urX}']= generate[0]

        world['world'][dimention][f'{urZ}_{urX}']= generate[1]
        with open('worlds'+worldName+'.json', 'w') as opnr:
            opnr.write(json.dumps(world, indent=4))

    elif f'{urZ}_{urX}' not in loadedWorld[dimention].keys():
        loadedWorld[dimention][f'{urZ}_{urX}']= []
        for yi, y in enumerate(world['world'][dimention][f'{urZ}_{urX}']):
            loadedWorld[dimention][f'{urZ}_{urX}'].append([])
            for zi, z in enumerate(y):
                loadedWorld[dimention][f'{urZ}_{urX}'][yi].append([])
                for x in z:
                    loadedWorld[dimention][f'{urZ}_{urX}'][yi][zi].append(blocks[x['id']](x))
                    #@funcNewChunk

def generator(urX, urZ):
#$funcGeneration
    newMatrix = []
    newMatrixSaver = []
    for y in range(chunkDimY):
        newMatrix.append([])
        newMatrixSaver.append([])
        for z in range (chunkDimZ):
            newMatrix[y].append([])
            newMatrixSaver[y].append([])
            for x in range(chunkDimX):
                for generate in generation["d0"]:
                    generated= generate({'urChunk':[urZ, urX], 'urPos':[y,z,x], 'knownWorld':world['seed']})
                    newMatrix[y][z].append(blocks[generated]())
                    newMatrixSaver[y][z].append(blocks[generated].default)


    return [newMatrix, newMatrixSaver]

#@funcCutOut

#@functions

while True:
#$mainLoop

    keys = list(pygame.key.get_pressed())

    for event in pygame.event.get():
        if keys[pygame.KSCAN_E] == 1:
            render('walk')
            

        if event.type == pygame.QUIT: 
            sys.exit()
    
        if keys[pygame.KSCAN_J] == 1:
            oofsetX = 600
            oofsetZ = 600
            render('walk')

        if keys[pygame.KSCAN_C] == 1:
            print('\n\nx: '+ str(int(oofsetX/100)) +'\nz: '+str(int(oofsetZ/50)))
            print('\nChunkX: '+ str(int(oofsetX/1200)) +'\nChunkZ: '+str(int(oofsetZ/1200)))

    
    if 1 in keys:

        if keys [pygame.KSCAN_A] == 1:
            oofsetX -= 5
            oofsetXR -= 5
            walkAnim = not walkAnim
            render('walk')
        elif keys [pygame.KSCAN_D] == 1:
            oofsetX += 5
            oofsetXR += 5
            walkAnim = not walkAnim
            render('walk')
        elif keys [pygame.KSCAN_W] == 1:
            oofsetZ -= 5
            oofsetZR -= 5
            walkAnim = not walkAnim
            render('walk')
        elif keys [pygame.KSCAN_S] == 1:
            oofsetZ += 5
            oofsetZR += 5
            walkAnim = not walkAnim
            render('walk')

#@mainLoop