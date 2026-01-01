import camera as cam
import canvas as cv
import viewport as vp
import sphere as sph
import scene
import math


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


def TraceRay(O, D, t_min, t_max,sc):
    closest_t = math.inf
    closest_sphere = None
    for sphere in sc.spheres :
        t1, t2 = IntersectRaySphere(O, D, sphere)
        if t1 >= t_min and t1 <= t_max and t1 < closest_t :
            closest_t = t1
            closest_sphere = sphere
        
        if t2 >= t_min and t2 <= t_max and t2 < closest_t :
            closest_t = t2
            closest_sphere = sphere
        
    
    if closest_sphere == None :
       return (255,255,255)
    
    return closest_sphere.color







O = (0, 0, 0)
canvas = cv.canvas(600,600)
viewport = vp.viewport(canvas)
redSphere = sph.Sphere((0,-1,3),1,(255,0,0))
blueSphere = sph.Sphere((2, 0, 4),1,(0, 0, 255))
greenSphere = sph.Sphere((-2, 0, 4),1,(0, 255, 0))
sc = scene.scene([redSphere,blueSphere,greenSphere],1,1,1)

for x in range(-canvas.width//2,(canvas.width//2)):
    for y in range(-canvas.height//2,(canvas.height//2)):
        D = viewport.CanvasToViewport(x,y)
        color = TraceRay(O, D, 1, math.inf,sc)
        canvas.putPixel(x, y, color)

canvas.createImage()

# for cx in range(canvas.width):
#     viewport.x = cx * (viewport.width/canvas.width)
#     for cy in range(canvas.height):
#         viewport.y = cy * (viewport.height/canvas.height)

