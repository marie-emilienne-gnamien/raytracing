import math
from vector import dot, sub, scale, length, normalize

class scene:
    def __init__(self, spheres, vpX, vpY, projectionPlaneD, lights=None):
        """Container for scene objects.
        - spheres: list of Sphere objects (must have .center and .radius)
        - vpX, vpY: viewport dimensions
        - projectionPlaneD: projection distance
        - lights: optional list of light objects (each may have attributes type, intensity, position, direction)
        """
        self.spheres = spheres
        self.lights = lights or []
        self.vpX = vpX
        self.vpY = vpY
        self.projectionPlaneD = projectionPlaneD

    # --- ray/sphere intersection (returns closest sphere and t) ---
    def FindClosestIntersection(self, O, D, t_min, t_max):
        closest_t = float('inf')
        closest_sphere = None
        for sphere in self.spheres:
            # solve quadratic for intersection
            CO = sub(O, sphere.center)
            a = dot(D, D)
            b = 2 * dot(CO, D)
            c = dot(CO, CO) - sphere.radius * sphere.radius

            discriminant = b*b - 4*a*c
            if discriminant < 0:
                continue
            sqrt_disc = math.sqrt(discriminant)
            t1 = (-b + sqrt_disc) / (2*a)
            t2 = (-b - sqrt_disc) / (2*a)

            for t in (t1, t2):
                if t_min <= t <= t_max and t < closest_t:
                    closest_t = t
                    closest_sphere = sphere

        return closest_sphere, closest_t

    # --- simple lighting model ---
    def compute_lighting(self, point, normal, view_vector, specular):
        """Compute lighting at a point.
        Accepts lights with attributes:
          - type: 'ambient', 'point', or 'directional'
          - intensity: float
          - position: (x,y,z) for point lights
          - direction: (x,y,z) for directional lights
        specular: shininess or -1 for no specular
        """
        intensity = 0.0
        for light in self.lights:
            ltype = getattr(light, 'type', None)
            lint = getattr(light, 'intensity', 0)

            if ltype == 'ambient':
                intensity += lint
                continue

            if ltype == 'point':
                L = sub(light.position, point)
                t_max = 1.0
            elif ltype == 'directional':
                # assume light.direction is the direction *to* the light
                L = light.direction
                t_max = float('inf')
            else:
                continue

            # shadow check
            L_dir = normalize(L)
            shadow_sphere, shadow_t = self.FindClosestIntersection(point, L_dir, 0.001, t_max)
            if shadow_sphere is not None:
                continue

            # diffuse
            n_dot_l = dot(normal, L_dir)
            if n_dot_l > 0:
                intensity += lint * (n_dot_l / (length(normal) or 1.0))

            # specular
            if specular != -1 and n_dot_l > 0:
                # R = 2*(N dot L)*N - L
                R = sub(scale(normal, 2*n_dot_l), L_dir)
                r_dot_v = dot(R, view_vector)
                if r_dot_v > 0:
                    intensity += lint * ((r_dot_v / (length(R) * length(view_vector) or 1.0)) ** specular)

        return intensity