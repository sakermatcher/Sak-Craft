import json
from helpers.functions import pearl, joinChunks
from copy import deepcopy

class d0():
    def grass(args):

        final= deepcopy(args['defChunk'])

        for z in range(args['chunkLen'][1]):
            for x in range(args['chunkLen'][2]):
                perlin= pearl(1, args['seed'], args['urChunk'][0], args['urChunk'][1], 3, z, x, args['chunkLen'][0], args['chunkLen'][1], 3)
                if perlin > 30:
                    for y in range(3):
                        final[y][z][x]= 'vanilla:grass'

                elif perlin < 30 and perlin > 0:
                    for y in range(2):
                        final[y][z][x]= 'vanilla:grass'
                
                else:
                    final[0][z][x]= 'vanilla:grass'
        return final

            


    def trees(args):

        return ''#joinChunks(1, args['urChunk'], args['worldName'], args['dimention'], deepcopy(args), 1, treeHelper)


def treeHelper(group, urChunkZX, args):
    print(len(group))
    exit()
    for z in range(urChunkZX[0][0], urChunkZX[0][1]):
        for x in range(urChunkZX[1][0], urChunkZX[1][1]):
            Break= True
            if group[2][z][x] == 'vanilla:grass':
                Break= False
                for inZ in range(z, z+3): 
                    for inX in range(x, x+3):
                        if group[3][inZ][inX] == 'vanilla:air':
                            Break= True
                            break
                    if Break:
                        break
            if Break == False:
                group[3][z][x]= 'vanilla:log'
                group[4][z][x]= 'vanilla:log'
    return group
                
            



