import random
import math
from PIL import Image




def renormalize(n, range1, range2):
    delta1 = range1[1] - range1[0]
    delta2 = range2[1] - range2[0]
    return (delta2 * (n - range1[0]) / delta1) + range2[0]


random.seed()


class X:
    @staticmethod
    def eval(x, y):
        return x

    def __str__(self):
        return "x"


class Y:
    @staticmethod
    def eval(x, y):
        return y

    def __str__(self):
        return "y"


class SinPi:
    def __init__(self, prob):
        self.arg = buildexpression(prob * prob)

    def __str__(self):
        return "sin(pi*" + str(self.arg) + ")"

    def eval(self, x, y):
        return math.sin(math.pi * self.arg.eval(x, y))


class ArcSinPi:
    def __init__(self, prob):
        self.arg = buildexpression(prob * prob)

    def __str__(self):
        return "arcsin(pi*" + str(self.arg) + ")"

    def eval(self, x, y):
        return math.asin(math.sin(math.pi * self.arg.eval(x, y)))


class CosPi:
    def __init__(self, prob):
        self.arg = buildexpression(prob * prob)

    def __str__(self):
        return "cos(pi*" + str(self.arg) + ")"

    def eval(self, x, y):
        return math.cos(math.pi * self.arg.eval(x, y))


class ArcCosPi:
    def __init__(self, prob):
        self.arg = buildexpression(prob * prob)

    def __str__(self):
        return "acos(pi*" + str(self.arg) + ")"

    def eval(self, x, y):
        return math.acos(math.cos(math.pi * self.arg.eval(x, y)))

class TanPi:
    def __init__(self, prob):
        self.arg = buildexpression(prob * prob)

    def __str__(self):
        return "tan(pi*" + str(self.arg) + ")"

    def eval(self, x, y):
        return math.tan(math.pi * self.arg.eval(x, y))


class Times:
    def __init__(self, prob):
        self.lhs = buildexpression(prob * prob)
        self.rhs = buildexpression(prob * prob)

    def __str__(self):
        print(self.lhs)
        print(self.rhs)
        return "(" + str(self.lhs) + "*" + str(self.rhs) + ")"

    def eval(self, x, y):
        return self.lhs.eval(x, y) * self.rhs.eval(x, y)


class Divide:
    def __init__(self, prob):
        self.arg = buildexpression(prob * prob)
        
    def __str__(self):
        return str(self.arg) + "/2"

    def eval(self, x, y):
        return self.arg.eval(x, y) / 2


def buildexpression(prob=.99):
     if random.random() < prob:
        return random.choice([SinPi, CosPi, ArcSinPi, ArcCosPi, TanPi, Times, Divide])(prob)
     else:
        return random.choice([X, Y])()


def plotintensity(exp, pixelsperunit=600):
    canvaswidth = 2 * pixelsperunit + 1
    canvas = Image.new("L", (canvaswidth, canvaswidth))

    for py in range(canvaswidth):
        for px in range(canvaswidth):
            # Convert pixel location to [-1,1] coordinates
            x = float(px - pixelsperunit) / pixelsperunit
            y = -float(py - pixelsperunit) / pixelsperunit
            z = exp.eval(x, y)
            # Scale [-1,1] result to [0,255].
            intensity = int(z * 127.5 + 127.5)
            # intensity = int(z * 127.5 + 50)
            # intensity = int(z%255)
            # print(z)
            # intensity = int(z * random.randint(0,255))
            point = (px, py)
            canvas.putpixel(point, intensity)

    return canvas


def plotcolor(redexpression, greenexpression, blueexpression, blackexpression, pixelsperunit=600):
    redplane = plotintensity(redexpression, pixelsperunit)
    greenplane = plotintensity(greenexpression, pixelsperunit)
    blueplane = plotintensity(blueexpression, pixelsperunit)
    blackplane = plotintensity(blackexpression, pixelsperunit)
    randoSelect = random.randint(0,3)
    
    if (randoSelect == 0):
      return Image.merge("RGB", (redplane, greenplane, blueplane))
    elif (randoSelect == 1):
       return Image.merge("CMYK", (redplane, greenplane, blueplane, blackplane))
    elif (randoSelect == 2):
      return Image.merge("HSV", (redplane, greenplane, blueplane)).convert("RGB")  
    else:
      return Image.merge("YCbCr", (redplane, greenplane, blueplane))


def makeimage(numberofimages=20):
    with open("eqns.txt", 'w') as eqnsFile:
        for i in range(numberofimages):
            redexpression = buildexpression(random.uniform(.1, .9))
            greenexpression = buildexpression(random.uniform(.1, .9))
            blueexpression = buildexpression(random.uniform(.1, .9))
            blackexpression = buildexpression(random.uniform(.4, .9))

            eqnsFile.write("img" + str(i) + ":\n")
            eqnsFile.write("red = " + str(redexpression) + "\n")
            eqnsFile.write("green = " + str(greenexpression) + "\n")
            eqnsFile.write("blue = " + str(blueexpression) + "\n")
            eqnsFile.write("black = " + str(blackexpression) + "\n\n")
            print("equation list has been made")
            # image = plotcolor(redexpression, greenexpression, blueexpression)
            image = plotcolor(redexpression, greenexpression, blueexpression, blackexpression)
            image.save("img/ze800-" + str(i) + ".jpg", "JPEG")
            print("Image " + str(i) + " has been made")
            # image.save("img/imgPO-" + str(i) + ".png", "PNG")


makeimage(800)
