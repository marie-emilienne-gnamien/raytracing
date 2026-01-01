
class viewport:
    def __init__(self,canvas):
        self.width = 1
        self.height = 1
        self.distance = 1
        self.x = 0
        self.y = 0
        self.z = self.distance
        self.canvas = canvas
    
    def CanvasToViewport(self,x,y):
        return (x*self.width/self.canvas.width,y*self.height/self.canvas.height,self.distance)
    
    