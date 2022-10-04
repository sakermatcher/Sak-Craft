class air():
    default= {'id':"vanilla:air", 'name':"Air"}
    def __init__(self, args=default) -> None:
        self.args= args
        self.texture= "vanilla:air"

class grass():
    default= {'id':"vanilla:grass", 'name':"Grass"}
    def __init__(self, args=default) -> None:
        self.args= args
        self.texture= "vanilla:grass"
        self.hitbox=[[[0,0,0],[100,100,100]]]

class log():
    default= {'id':"vanilla:log", 'name':"Log"}
    def __init__(self, args=default) -> None:
        self.args= args
        self.texture= "vanilla:log"
        self.hitbox=[[[0,0,0],[100,100,100]]]