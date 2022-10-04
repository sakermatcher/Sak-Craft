import json
from copy import deepcopy

def pearl(layer, seed, chunkZ, chunkX, urY, urZ, urX, chunkZLen, chunkXLen, variation):
    """
    Inputs a position and a layer and returns its perlin value as a float, after some bruteforcing Ive found
    that it PROBABLY has a max value of 60 and min of -60, altho unsure so be careful about that

    WARNING: some layers like 100 or 200, etc. may always return 0.0, test beforehand
    to check if your layer works
    """
    from perlin_noise import PerlinNoise
    noise = PerlinNoise(octaves=layer, seed=seed)

    z= chunkZ*chunkZLen + urZ
    x= chunkX*chunkXLen + urX
    y=urY

    variation= [1,5,10,25,50,100][variation]

    final= noise([y/variation, z/variation, x/variation])*100

    if final == 0.0:
        x += 10
        if noise([y/100, z/100, x/100])*100 == 0.0:#Double check in case of a exception
            print('Error calling pearl function, probably due to a faulty layer value; 0.0 will always be returned with the selected layer value,\n add 1 to the layer or just change it...\n Faulty layer: '+str(layer))
            exit()

    return final

def generator(urChZ, urChX, generation, chunkDimY, chunkDimZ, chunkDimX, dimFile, blocks, dimention, worldName, wrldFile, defChunk):
    newMatrix = []
    newMatrixSaver = []
    generated= None

    for generate in generation[dimention]:
        generated= generate({'seed':wrldFile['seed'], 'urChunk':[urChZ, urChX], 'worldFile':wrldFile, 'chunkLen': [chunkDimY, chunkDimZ, chunkDimX], 'building':newMatrixSaver, 'dimention':dimention, 'worldName':worldName, 'blocks':blocks, 'generation':generation, 'workingOn':generated, 'dimFile':dimFile, 'defChunk':deepcopy(defChunk)})
    for y in range(chunkDimY):
        newMatrix.append([])
        newMatrixSaver.append([])
        for z in range (chunkDimZ):
            newMatrix[y].append([])
            newMatrixSaver[y].append([])
            for x in range(chunkDimX):
                try:      
                    newMatrix[y][z].append(blocks[generated[y][z][x]]())
                except:
                    print(generated[y][z][x])
                    exit()
                newMatrixSaver[y][z].append(blocks[generated[y][z][x]].default)


    return [newMatrix, newMatrixSaver, generated]

def joinChunks(radious, oriCh, worldName, dimention, args, lastLayer, ToDo):
    
    toGenerate= {dimention:[]}
    for layer in range(lastLayer):
        toGenerate[dimention].append(args['generation'][dimention][layer])
    starterZX= [oriCh[0]-radious, oriCh[1]-radious]
    with open('worlds/'+worldName+'.json', 'r') as rdr:
        world= json.loads(rdr.read())
    
    final=[]
    preFinal=[]
    preFinal1=[]
    for y in range(args['chunkLen'][0]):
        preFinal.append([])
        preFinal1.append([])
        final.append([])
        for z in range(args['chunkLen'][1]):
            preFinal[y].append([])
    
    for z in range(starterZX[0], oriCh[0]+radious+1):
        preFinalY= preFinal1.copy()
        preFinalZ= preFinal.copy()
        
        for x in range(starterZX[1], oriCh[1]+radious+1):
            if f'{z}_{x}' not in world['world'][dimention]:
                generated= generator(z, x, toGenerate, args['chunkLen'][0], args['chunkLen'][1], args['chunkLen'][2], world, args['blocks'], args['dimention'], worldName, deepcopy(args['defChunk']))
                world['world'][dimention][f'{z}_{x}']= generated[2]
            for inY in range(args['chunkLen'][0]):
                for inZ in range(args['chunkLen'][1]):
                    preFinalZ[inY] += generated[2][inY][inZ]
                preFinalY[inY] += (preFinal)
        for inY in range(args['chunkLen'][0]):
            final[inY] += preFinalY

    iterable=[[radious*args['chunkLen'][1], radious*args['chunkLen'][1] + args['chunkLen'][1]],
    [radious*args['chunkLen'][2], radious*args['chunkLen'][2] + args['chunkLen'][2]]]
    done= ToDo(final, iterable, args)

    ffinal=[]
    print(len(done[0][0]))
    for y in range(args['chunkLen'][0]):
        ffinal.append([])
        for zi, z in enumerate(range(iterable[0][0], iterable[0][1])):
            ffinal[y].append([])
            for x in range(iterable[1][0], iterable[1][1]):
                ffinal[y][zi].append(done[y][z][x])

    return ffinal
