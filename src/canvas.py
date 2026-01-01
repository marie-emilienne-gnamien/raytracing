import os

class canvas:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.toile = []
        for y in range(self.height):
            l = []
            for x in range(self.width):
                l.append((255,255,255))
            self.toile.append(l)

    def putPixel(self, x, y, color): #color has this form (example: (255 255 255)) (R G B) a value is > 255 then it is 255 and value < 0 is 0
        x_index = self.width // 2 + x
        y_index = self.height // 2 - y
        # print(x_index)
        # print(y_index)
        if x_index >= self.width or y_index >= self.height or x_index < 0 or y_index < 0:
            return
        else:
            self.toile[y_index][x_index] = color

    def createImage(self):
        filename = "image.txt"
        path = os.path.join("output",filename)
        with open(path,mode='w',encoding='utf-8') as final:
            final.write("P3\n")
            final.write(str(self.width) + " " + str(self.height) + "\n")
            final.write("255\n")

            for line in self.toile:
                for i in range(len(line)):
                    clr = str(line[i])
                    clr = clr.replace(",","")
                    # print(clr[1:-1])
                    final.write(clr[1:-1])
                    final.write("\n")
        newpath = os.path.join("output","image.ppm")
        os.rename(path,newpath)

                
                
                


