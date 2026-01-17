class Light:
    def __init__(self, ltype, intensity, position=None, direction=None):
        # ltype: 'ambient', 'point', 'directional'
        self.type = ltype
        self.intensity = intensity
        self.position = position
        self.direction = direction
