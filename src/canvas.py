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

    def createImage(self, open_image=False, outdir=None, save_png=False):
        # Write directly to image.ppm inside the repository output folder by default
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        if outdir is None:
            outdir = os.path.join(repo_root, "output")
        os.makedirs(outdir, exist_ok=True)
        path = os.path.join(outdir, "image.ppm")

        with open(path, mode='w', encoding='utf-8') as final:
            final.write("P3\n")
            final.write(f"{self.width} {self.height}\n")
            final.write("255\n")

            for line in self.toile:
                for i in range(len(line)):
                    clr = str(line[i])
                    clr = clr.replace(",", "")
                    final.write(clr[1:-1])
                    final.write("\n")

        png_path = None
        if save_png:
            try:
                from PIL import Image
                img = Image.open(path)
                png_path = os.path.join(outdir, "image.png")
                img.save(png_path)
            except Exception as exc:
                # Pillow not installed or saving failed; skip PNG silently
                print("PNG export skipped:", exc)
                png_path = None

        if open_image:
            try:
                target = png_path if png_path else path
                if os.name == 'nt':
                    os.startfile(target)
                else:
                    import subprocess, sys
                    opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
                    subprocess.run([opener, target], check=False)
            except Exception:
                pass

                
                
                


