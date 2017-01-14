import random
import math
from PIL import Image

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
        return "(" + str(self.lhs) + "*" + str(self.rhs) + ")"

    def eval(self, x, y):
        return self.lhs.eval(x, y) * self.rhs.eval(x, y)


class Divide:
    def __init__(self, prob):
        self.arg = buildexpression(prob * prob)

    def __str__(self):
        return str(self.arg) + "/ 2"

    def eval(self, x, y):
        return self.arg.eval(x, y) / 2


def buildexpression(prob=.99):
    if random.random() < prob:
        return random.choice([SinPi, CosPi, ArcSinPi, Times, Divide])(prob)
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
            canvas.putpixel((px, py), intensity)

    return canvas


def plotcolor(redexpression, greenexpression, blueexpression, blackexpression, pixelsperunit=600):
    redplane = plotintensity(redexpression, pixelsperunit)
    greenplane = plotintensity(greenexpression, pixelsperunit)
    blueplane = plotintensity(blueexpression, pixelsperunit)
    blackplane = plotintensity(blackexpression, pixelsperunit)
    # return Image.merge("RGB", (redplane, greenplane, blueplane))
    return Image.merge("CMYK", (redplane, greenplane, blueplane, blackplane))


def makeimage(numberofimages=20):
    with open("eqns.txt", 'w') as eqnsFile:
        for i in range(numberofimages):
            redexpression = buildexpression(random.uniform(.1, .9))
            greenexpression = buildexpression(random.uniform(.1, .9))
            blueexpression = buildexpression(random.uniform(.8, 1))
            blackexpression = buildexpression(random.uniform(.4, 1))

            eqnsFile.write("img" + str(i) + ":\n")
            eqnsFile.write("red = " + str(redexpression) + "\n")
            eqnsFile.write("green = " + str(greenexpression) + "\n")
            eqnsFile.write("blue = " + str(blueexpression) + "\n")
            eqnsFile.write("black = " + str(blackexpression) + "\n\n")
            # image = plotcolor(redexpression, greenexpression, blueexpression)
            image = plotcolor(redexpression, greenexpression, blueexpression, blackexpression)
            image.save("img/imgJ-" + str(i) + ".jpg", "JPEG")
            # image.save("img/imgP-" + str(i) + ".png", "PNG")


makeimage(10)
