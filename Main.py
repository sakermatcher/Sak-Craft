from os import mkdir
import PySimpleGUI as sg
import json
import random
from copy import deepcopy
from Engine import engine

out= False
usedL= 'main'
layouts= ["main", "play"]
sg.theme('Dark Grey 11')

rand= ''
for i in range(10):
    rand+= str(random.randint(1,100))

rand= int(rand)

newID= ''
letters= 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'

for i in range(15):
    newID+= letters[random.randint(0,51)]


while not out:

    with open('settings.json', 'r') as opnr:
        sett= json.load(opnr)

    layoutMain= [
                [sg.Button('SINGLEPLAYER', key='play')],
                [sg.Button('MULTIPLAYER', key='multi')],
                [sg.Button('SETTINGS', key='settings')],
                [sg.Button('PORFILE', key='porfile')]
            ]

    layoutSingle= [
                [sg.Button('<BACK', key='main', button_color='blue'), sg.Button('NEW WORLD', key='new', button_color='green')]
            ]

    layoutPorfile= [
        [sg.Button('<BACK', key='main', button_color='blue')]
    ]

    layoutNew= [
        [sg.Button('<BACK', key='play', button_color='blue')],
        [sg.Text('World Name:'), sg.Input('New World', key=('name'))],
        [sg.Text('Seed:'), sg.Input(str(rand), key='seed')],
        [sg.HSeparator()],
        [sg.Text('ADVANCED:')],
        [sg.Text('Chunk Sizes:')],
        [sg.Text('X:'), sg.Input('12', (3,1), key='x'), sg.Text('Z:'), sg.Input('24', (3,1), key='z'), sg.Text('Y:'), sg.Input('30', (3,1), key='y')],
        [sg.HSeparator()],
        [sg.Button('GENERATE', size=(40,2), key='generate', button_color='green')]
    ]

    for i in sett['worlds']:
        try:
            with open(f'worlds/{i}/world.json', 'r') as opnr:
                name= json.load(opnr)['name']
            layoutSingle.append([sg.Button(f'{name}', size=(30,1), key=f'0{i}'), sg.Button('edit', size=(4,1), key=f'1{i}')])
        except:
            print(f'Error: world ID: "{i}" not found')

    layoutEdit= []

    if usedL == 'edit':
        with open(f'worlds/{goTo}/world.json', 'r') as opnr:
            world= json.load(opnr)
        layoutEdit= [
            [sg.Button('<BACK', key='play', button_color='blue')],
            [sg.Text('Name: '), sg.Input(world['name'], (10,1), k='name')],
            [sg.Text('Seed: '+str(world['seed']))],
            [sg.Text('ID: ' + goTo)]
        ]


    layouts= {
        "main":layoutMain,
        "play":layoutSingle,
        "multi":deepcopy(layoutMain) + [[sg.Text('Multiplayer is not out yet!', text_color='red')]],
        "porfile": layoutPorfile,
        "new": layoutNew,
        "edit":layoutEdit
    }

    window= sg.Window('Ygame', deepcopy(layouts[usedL]), resizable=True, size=(500,500), element_justification='center')
    
    while True:

        with open('settings.json', 'r') as opnr:
            settings=json.load(opnr)
            player= settings['player']

        event, values= window.read(close=True)

        if event[0] == '0' and event[1:] in settings['worlds']:
            goTo= event[1:]
            out=True
        elif event[0] == '1' and event[1:] in settings['worlds']:
            usedL= 'edit'
            goTo= event[1:]

        elif event in layouts:
            usedL= event
        
        elif event == 'generate':
            out= True
            goTo= newID
            try:
                mkdir(f'worlds/{newID}')
                mkdir(f'worlds/{newID}/dims')#Make the new world folders
            
                settings['worlds'].append(newID)
                with open('settings.json', 'w') as opnr:
                    opnr.write(json.dumps(settings, indent=4))

            except:
                print('Maybe the dir allready exists')
                exit()

            with open('worlds/default/world.json', 'r') as opnr: #Read default world
                default= json.load(opnr)
            default['seed']= int(values['seed'])
            default['name']= values['name']
            default['chunkSize']['x']= int(values['x'])
            default['chunkSize']['z']= int(values['z'])
            default['chunkSize']['y']= int(values['y'])
            with open(f'worlds/{newID}/world.json', 'w+') as opnr: #Write the world file
                opnr.write(json.dumps(default, indent=4))

            with open('worlds/default/players.json', 'r') as opnr: #Read default players file
                default= json.load(opnr)
            default[player['tag']]= {'x':600, 'z':600, 'y':0, 'dim':'d0'}

            with open(f'worlds/{newID}/players.json', 'w+') as opnr: #Write the players file
                opnr.write(json.dumps(default, indent=4))

        elif event == sg.WIN_CLOSED:
            exit()

        break

toRun= engine(goTo)
toRun.run()