import camera as cam
import canvas as cv
import viewport as vp
import sphere as sph
import scene
import math
from vector import normalize, length, clamp


def dot(a,b):
    return (a[0]*b[0])+(a[1]*b[1])+(a[2]*b[2])

def IntersectRaySphere(O, D, sphere) :
    r = sphere.radius
    CO = (O[0] - sphere.center[0],O[1] - sphere.center[1],O[2] - sphere.center[2])

    a = dot(D, D)
    b = 2*dot(CO, D)
    c = dot(CO, CO) - r*r
    
    discriminant = b*b - 4*a*c
    if discriminant < 0 :
        return math.inf, math.inf
    

    t1 = (-b + math.sqrt(discriminant)) / (2*a)
    t2 = (-b - math.sqrt(discriminant)) / (2*a)
    return t1, t2


def TraceRay(O, D, t_min, t_max, sc):
    # Use scene.FindClosestIntersection to get the nearest sphere and t
    sphere, t = sc.FindClosestIntersection(O, D, t_min, t_max)
    if sphere is None:
        return (255, 255, 255)

    # Compute intersection point P = O + t * D
    P = (O[0] + D[0]*t, O[1] + D[1]*t, O[2] + D[2]*t)
    # Normal at P
    N = (P[0] - sphere.center[0], P[1] - sphere.center[1], P[2] - sphere.center[2])

    N = normalize(N)
    V = normalize((-D[0], -D[1], -D[2]))

    intensity = sc.compute_lighting(P, N, V, sphere.specular)

    # Apply lighting to the sphere color
    r = clamp(sphere.color[0] * intensity)
    g = clamp(sphere.color[1] * intensity)
    b = clamp(sphere.color[2] * intensity)
    return (r, g, b)







O = (0, 0, 0)
canvas = cv.canvas(600,600)
viewport = vp.viewport(canvas)
redSphere = sph.Sphere((0,-1,3),1,(255,0,0), specular=500)
blueSphere = sph.Sphere((2, 0, 4),1,(0, 0, 255), specular=500)
greenSphere = sph.Sphere((-2, 0, 4),1,(0, 255, 0), specular=10)
yellowSphere = sph.Sphere((0, -5001, 0), 5000, (255, 255, 0), specular=0)

# Lights: ambient + one point light + directional
import light as lt
lights = [
    lt.Light('ambient', 0.2),
    lt.Light('point', 0.6, position=(2,1,0)),
    lt.Light('directional', 0.2, direction=(1,4,4))
]

sc = scene.scene([redSphere,blueSphere,greenSphere,yellowSphere],1,1,1, lights=lights)

for x in range(-canvas.width//2,(canvas.width//2)):
    for y in range(-canvas.height//2,(canvas.height//2)):
        D = viewport.CanvasToViewport(x,y)
        color = TraceRay(O, D, 1, math.inf,sc)
        canvas.putPixel(x, y, color)

canvas.createImage(open_image=True, save_png=True)

# for cx in range(canvas.width):
#     viewport.x = cx * (viewport.width/canvas.width)
#     for cy in range(canvas.height):
#         viewport.y = cy * (viewport.height/canvas.height)
