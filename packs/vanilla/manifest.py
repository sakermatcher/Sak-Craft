from packs.vanilla.blocks import air, grass
from packs.vanilla.generation import d0
import pygame


manifest= {
    "version":[1,0,0],
    "description":"Vanilla",
    "uuid":"",
    "stuff":{
        "textures":{
            "vanilla:air": None,
            "vanilla:grass":pygame.image.load("packs/vanilla/textures/blocks/grass.png")
        },
        "items":{

        },
        "blocks":{
            "vanilla:air":air,
            "vanilla:grass":grass
        },
        "generation":{
            "d0": [d0.layer0]
        }
    }
}
