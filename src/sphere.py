class Sphere:
    def __init__(self, center, radius, color, specular=-1):
        self.center = center
        self.radius = radius
        self.color = color
        # specular: shininess exponent, -1 = no specular
        self.specular = specular