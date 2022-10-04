from packs.vanilla.blocks import air, grass, log
from packs.vanilla.generation import d0
import pygame


manifest= {
    "version":[0,0,1],
    "name":"Vanilla",
    "description":"Vanilla Stuff",
    "stuff":{
        "textures":{
            "vanilla:air": None,
            "vanilla:grass":pygame.image.load("packs/vanilla/textures/blocks/grass.png"),
            "vanilla:log":pygame.image.load("packs/vanilla/textures/blocks/log.png")
        },
        "items":{

        },
        "blocks":{
            "vanilla:air":air,
            "vanilla:grass":grass,
            "vanilla:log":log
        },
        "generation":{
            "d0": {
                0:[
                    d0.grass
                ]
            }
        }
    }
}
