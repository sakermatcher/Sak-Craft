#$imports

import json
import pygame
import math
import PySimpleGUI as sg
import importlib
from helpers.functions import generator
from copy import deepcopy

class engine():
    def __init__(self, wrldID) -> None:
        self.wrldPath= f'worlds/{wrldID}/' #Shortened path to the world folder

        pygame.init() #Start Pygame
        self.size= width, height = 1000, 800 #Screen size
        self.walkAnim= True #To say if your character texture is the one with the left leg or the one with the right one

        with open(self.wrldPath+'world.json', 'r') as opnr:
            self.worldFile= json.load(opnr)
        with open(self.wrldPath+'players.json', 'r') as opnr:
            self.playersFile= json.load(opnr)

        self.chunkDimX= self.worldFile['chunkSize']['x'] #Set x z and y chunk dimentions
        self.chunkDimZ= self.worldFile['chunkSize']['z']
        self.chunkDimY= self.worldFile['chunkSize']['y']

        self.oofsetXR, self.oofsetZR= 600, 600 #Position of the player in the CHUNK expressed in pixels
        self.background= self.worldFile['background'] #Background/sky Color

        with open('settings.json', 'r') as opnr:
            self.settingsFile= json.load(opnr)
        self.nameTag= self.settingsFile['player']['tag']

        self.seed= self.worldFile['seed']

        self.blocks={} #List of all blocks in world
        self.items={} #List of all items in world
        self.textures={} #List of all textures in world
        self.generation= {} #List of every generation layer

        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self.events = pygame.event.get()

        self.oofsetX= self.playersFile[self.nameTag]['x'] #x position of the player in the WORLD expressed in pixels
        self.oofsetZ= self.playersFile[self.nameTag]['z'] #z position of the player in the WORLD expressed in pixels
        self.dimention= self.playersFile[self.nameTag]['dim']

        try:
            with open (f'{self.wrldPath}dims/{self.dimention}.json', 'r') as opnr:
                self.dimFile= json.load(opnr)
        except:
            self.dimFile= {}
            with open (f'{self.wrldPath}dims/{self.dimention}.json', 'w+') as opnr:
                opnr.write('{\n\n}')

        self.packs= self.worldFile['packs']

        self.defChunk= [] #A default chunk made so that when generating a new chunk you dont have to do the for loops again

        for y in range(self.chunkDimY):
            self.defChunk.append([])
            for z in range(self.chunkDimZ):
                self.defChunk[y].append([])
                for x in range(self.chunkDimX):
                    self.defChunk[y][z].append('vanilla:air')

        for pack in self.packs: #Add every thing from all the packs added in your world into one dictionary for each category
            for thing in importlib.import_module('packs.'+pack+'.manifest').manifest["stuff"]["blocks"].keys():
                self.blocks[thing] = importlib.import_module('packs.'+pack+'.manifest').manifest["stuff"]["blocks"][thing]
            for thing in importlib.import_module('packs.'+pack+'.manifest').manifest["stuff"]["items"].keys():
                self.items[thing] = importlib.import_module('packs.'+pack+'.manifest').manifest["stuff"]["items"][thing]
            for thing in importlib.import_module('packs.'+pack+'.manifest').manifest["stuff"]["textures"].keys():
                self.textures[thing] = importlib.import_module('packs.'+pack+'.manifest').manifest["stuff"]["textures"][thing]
            for thing in importlib.import_module('packs.'+pack+'.manifest').manifest["stuff"]["generation"].keys():
                self.generation[thing] = importlib.import_module('packs.'+pack+'.manifest').manifest["stuff"]["generation"][thing]

        self.defaultSteveR = pygame.image.load("helpers/player/steveR.png")
        self.defaultSteveL = pygame.image.load("helpers/player/steveL.png")
        
        self.unknownTexture= pygame.image.load("helpers/unknown.png").convert_alpha()

        self.loadedWorld= {'d0':{}}

        self.steveLrect = self.defaultSteveL.get_rect().move(450, 350)
        self.steveRrect = self.defaultSteveR.get_rect().move(450, 350)

        self.maxY = self.chunkDimY


    def render(self, type):
    #$funcRender
        first = False

        if type == 'walk':
            self.playersFile[self.nameTag]= {'x':self.oofsetX, 'z':self.oofsetZ, 'y': 0, 'dim':self.dimention}
            with open(self.wrldPath+'players.json', 'w') as opnr:
                opnr.write(json.dumps(self.playersFile, indent=4))

        urX = math.floor(self.oofsetX/100)
        urZ = math.floor(self.oofsetZ/50)
        urChunkX = math.ceil(urX/self.chunkDimX)
        urChunkZ = math.ceil(urZ/self.chunkDimZ)
        self.window['coords'].Update(f'X: {urChunkX} | Z: {urChunkZ}')

        if f'{urChunkZ}_{urChunkX}' not in self.loadedWorld[self.dimention].keys():
            self.loadedWorld= {}
            self.chunkChange(urChunkX, urChunkZ)
            self.oofsetXR = 100+(urX - urChunkX *self.chunkDimX)*100
            self.oofsetZR = 100+(urZ - urChunkZ *self.chunkDimZ)*50
            first= True

        if first == True:
            self.surf = pygame.image.load("helpers/bak.png").convert_alpha()
            for y in range(self.maxY):
                for z in range(self.chunkDimZ):
                    for x in range(self.chunkDimX):
                        try:
                            if z%2 == 0 and self.textures[self.loadedWorld[self.dimention][f'{urChunkZ}_{urChunkX}'][y][z][x].texture] != None: 
                                        
                                pygame.Surface.blit(self.surf, self.textures[self.loadedWorld[self.dimention][f'{urChunkZ}_{urChunkX}'][y][z][x].texture], dest=(x*100+500, z*40 - y*30 + 500))

                                    
                            elif self.textures[self.loadedWorld[self.dimention][f'{urChunkZ}_{urChunkX}'][y][z][x].texture] != None:
                                        
                                pygame.Surface.blit(self.surf, self.textures[self.loadedWorld[self.dimention][f'{urChunkZ}_{urChunkX}'][y][z][x].texture], dest=(x*100+550, z*40 - y*30 + 500))
                        except:

                            if z%2 == 0: 
                                        
                                pygame.Surface.blit(self.surf, self.unknownTexture, dest=(x*100+500, z*40 - y*30 + 500))

                                    
                            else:
                                        
                                pygame.Surface.blit(self.surf, self.unknownTexture, dest=(x*100+550, z*40 - y*30 + 500))

                            print(f'Texture not found for block at y:{y}, z:{z}, x:{x} | chunkZX: {urChunkZ}, {urChunkX} | ID: {self.loadedWorld[self.dimention][str(urChunkZ)+"_"+str(urChunkX)][y][z][x].default["id"]}')

        self.screen.fill(self.background)
        self.screen.blit(self.surf, dest=(-1000 - self.oofsetXR, -1000 - self.oofsetZR))
        if self.walkAnim == True:
            self.screen.blit(self.defaultSteveL, self.steveLrect)
        else:
            self.screen.blit(self.defaultSteveR, self.steveRrect)

        pygame.display.flip()
    #@funcRender

    def chunkChange(self, urChX:int, urChZ:int):
    #$funcChunkChange

        if self.dimention not in self.loadedWorld.keys():
            self.loadedWorld[self.dimention] = {}

        if f'{urChZ}_{urChX}' not in self.dimFile.keys():
            generate= generator(urChZ, urChX, self.generation, self.chunkDimY, self.chunkDimZ, self.chunkDimX, self.dimFile, self.blocks, self.dimention, self.wrldPath, self.worldFile, deepcopy(self.defChunk))
            self.loadedWorld[self.dimention][f'{urChZ}_{urChX}']= generate[0]

            self.dimFile[f'{urChZ}_{urChX}']= generate[1]
            with open(self.wrldPath+f'dims/{self.dimention}.json', 'w') as opnr:
                opnr.write(json.dumps(self.dimFile, indent=4))

        elif f'{urChZ}_{urChX}' not in self.loadedWorld[self.dimention].keys():
            self.loadedWorld[self.dimention][f'{urChZ}_{urChX}']= []
            for yi, y in enumerate(self.dimFile[f'{urChZ}_{urChX}']):
                self.loadedWorld[self.dimention][f'{urChZ}_{urChX}'].append([])
                for zi, z in enumerate(y):
                    self.loadedWorld[self.dimention][f'{urChZ}_{urChX}'][yi].append([])
                    for x in z:
                        self.loadedWorld[self.dimention][f'{urChZ}_{urChX}'][yi][zi].append(self.blocks[x['id']](x))
                        #@funcNewChunk

    #@funcCutOut

    #@functions

    

    def run(self):

        layoutCoords= [[sg.Text('X: 0 | Z: 0', key='coords')],
                    [sg.Text('Z:'), sg.Input('0', key='z')],
                    [sg.Text('X:'), sg.Input('0', key='x')],
                    [sg.Button('TP', key='tp')]
        ]

        self.window= sg.Window('Coords', layoutCoords, keep_on_top=True, location=(0,0))
        
        while True:
            #$mainLoop
            renderM= 'idle'

            event, values= self.window.read(timeout=0.000001)
            keys = list(pygame.key.get_pressed())

            if event == 'tp':
                self.oofsetX= int(values['x'])*1200
                self.oofsetZ= int(values['z'])*1200
                renderM= 'idle'
                
            if event == sg.WIN_CLOSED:
                exit()

            for gevent in pygame.event.get():

                if gevent.type == pygame.QUIT: 
                    exit()
                
            if 1 in keys:

                if keys[pygame.KSCAN_E] == 1:
                    renderM= 'idle'

                if keys[pygame.KSCAN_J] == 1:
                    self.oofsetX = 600
                    self.oofsetZ = 600
                    renderM= 'idle'

                if keys [pygame.KSCAN_A] == 1:
                    self.oofsetX -= 5
                    self.oofsetXR -= 5
                    self.walkAnim = not self.walkAnim
                    renderM= 'walk'
                elif keys [pygame.KSCAN_D] == 1:
                    self.oofsetX += 5
                    self.oofsetXR += 5
                    self.walkAnim = not self.walkAnim
                    renderM= 'walk'
                if keys [pygame.KSCAN_W] == 1:
                    self.oofsetZ -= 5
                    self.oofsetZR -= 5
                    self.walkAnim = not self.walkAnim
                    renderM= 'walk'
                elif keys [pygame.KSCAN_S] == 1:
                    self.oofsetZ += 5
                    self.oofsetZR += 5
                    self.walkAnim = not self.walkAnim
                    renderM= 'walk'

                if keys[pygame.KSCAN_0] == 1:
                    self.maxY= self.chunkDimY
                elif keys[pygame.KSCAN_1] == 1:
                    self.maxY= 1
                elif keys[pygame.KSCAN_2] == 1:
                    self.maxY= 2
                elif keys[pygame.KSCAN_3] == 1:
                    self.maxY= 3
                elif keys[pygame.KSCAN_4] == 1:
                    self.maxY= 4
                elif keys[pygame.KSCAN_5] == 1:
                    self.maxY= 5
                elif keys[pygame.KSCAN_6] == 1:
                    self.maxY= 6
                elif keys[pygame.KSCAN_7] == 1:
                    self.maxY= 7
                elif keys[pygame.KSCAN_8] == 1:
                    self.maxY= 8
                elif keys[pygame.KSCAN_9] == 1:
                    self.maxY= 9
                
            self.render(renderM)

            #@mainLoop