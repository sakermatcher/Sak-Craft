def pearl(urX, urZ, xpix, zpix, ypix, sed):
    from perlin_noise import PerlinNoise
    noise = PerlinNoise(octaves=1, seed=sed)
    
    mat = [[noise([i/xpix+urX, j/zpix+urZ]) for j in range(xpix)] for i in range(zpix)]

    for z in range (zpix):
        for x in range (xpix):
            for y in range (ypix):

                if mat[z][x] > 2/ypix * y -1 and mat[z][x] < 2/ypix * (y+1) -1:
                    mat[z][x] = y

            
    return(mat)

def structures(urX, urY, xpix, zpix, ypix, sed):
    from structures import structs
    
