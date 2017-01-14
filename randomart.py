import random
import math
from PIL import Image


random.seed()


class X:
    def eval(self, x, y):
        return x

    def __str__(self):
        return "x"


class Y:
    def eval(self, x, y):
        return y

    def __str__(self):
        return "y"


class SinPi:
    def __init__(self, prob):
        self.arg = buildExpr(prob * prob)

    def __str__(self):
        return "sin(pi*" + str(self.arg) + ")"

    def eval(self, x, y):
        return math.sin(math.pi * self.arg.eval(x, y))


class ArcSinPi:
    def __init__(self, prob):
        self.arg = buildExpr(prob * prob)

    def __str__(self):
        return "arcsin(pi*" + str(self.arg) + ")"

    def eval(self, x, y):
        return math.asin(math.sin(math.pi * self.arg.eval(x, y)))


class CosPi:
    def __init__(self, prob):
        self.arg = buildExpr(prob * prob)

    def __str__(self):
        return "cos(pi*" + str(self.arg) + ")"

    def eval(self, x, y):
        return math.cos(math.pi * self.arg.eval(x, y))


class TanPi:
    def __init__(self, prob):
        self.arg = buildExpr(prob * prob)

    def __str__(self):
        return "tan(pi*" + str(self.arg) + ")"

    def eval(self, x, y):
        return math.tan(math.pi * self.arg.eval(x, y))


class Times:
    def __init__(self, prob):
        self.lhs = buildExpr(prob * prob)
        self.rhs = buildExpr(prob * prob)

    def __str__(self):
        return "(" + str(self.lhs) + "*" + str(self.rhs) + ")"

    def eval(self, x, y):
        return self.lhs.eval(x, y) * self.rhs.eval(x, y)

class Divide:
    def __init__(self, prob):
        self.arg = buildExpr(prob * prob)

    def __str__(self):
        return str(self.arg) + "/ 2"

    def eval(self, x, y):
        return self.arg.eval(x, y)/2


def buildExpr(prob=.9):
    if random.random() < prob:
        return random.choice([SinPi, CosPi, ArcSinPi, Times, Divide])(prob)
    else:
        return random.choice([X, Y])()


def plotIntensity(exp, pixelsPerUnit=600):
    canvasWidth = 2 * pixelsPerUnit + 1
    canvas = Image.new("L", (canvasWidth, canvasWidth))

    for py in range(canvasWidth):
        for px in range(canvasWidth):
            # Convert pixel location to [-1,1] coordinates
            x = float(px - pixelsPerUnit) / pixelsPerUnit
            y = -float(py - pixelsPerUnit) / pixelsPerUnit
            z = exp.eval(x, y)
            # Scale [-1,1] result to [0,255].
            intensity = int(z * 127.5 + 127.5)
            #intensity = int(z * 127.5 + 50)
            canvas.putpixel((px, py), intensity)

    return canvas


def plotColor(redExp, greenExp, blueExp, blackExp, pixelsPerUnit=600):
    redPlane = plotIntensity(redExp, pixelsPerUnit)
    greenPlane = plotIntensity(greenExp, pixelsPerUnit)
    bluePlane = plotIntensity(blueExp, pixelsPerUnit)
    blackPlane = plotIntensity(blackExp, pixelsPerUnit)
    #return Image.merge("RGB", (redPlane, greenPlane, bluePlane))
    return Image.merge("CMYK", (redPlane, greenPlane, bluePlane, blackPlane))

def makeImage(numPics=20):
    with open("eqns.txt", 'w') as eqnsFile:
        for i in range(numPics):
            redExp = buildExpr(random.uniform(.1, .9))
            greenExp = buildExpr(random.uniform(.1, .9))
            blueExp = buildExpr(random.uniform(.8, 1))
            blackExp = buildExpr(random.uniform(.4, 1))

            eqnsFile.write("img" + str(i) + ":\n")
            eqnsFile.write("red = " + str(redExp) + "\n")
            eqnsFile.write("green = " + str(greenExp) + "\n")
            eqnsFile.write("blue = " + str(blueExp) + "\n")
            eqnsFile.write("black = " + str(blackExp) + "\n\n")
            #image = plotColor(redExp, greenExp, blueExp)
            image = plotColor(redExp, greenExp, blueExp, blackExp)
            image.save("psy2/img-T" + str(i) + ".jpg", "JPEG")
            #image.save("psy2/img-S" + str(i) + ".png", "PNG")


makeImage(10)
