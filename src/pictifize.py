import sys
import glob, os
from shutil import copy
import random
from random import randint
from PIL import Image


__author__="Kyle Valade"
__date__ ="$11-Dec-2011 4:32:20 PM$"

def main(argv=None):
    # make args later
    if argv is None:
        argv = sys.argv

    dir = "/home/k-dazzle/Documents/Programming/Lossifize/copies"
    original = "%s/%s" % (dir, "Refinery.jpg")

    originalImage = Image.open(original)

    size = originalImage.size
    newWidth = size[0] / 2
    newHeight = size[1] / 2

    resizedImage = originalImage.copy()
    resizedImage = resizedImage.resize((newWidth, newHeight))
    resizedImage.save("%s/%s" % (dir, "resized.jpg"))


    comparableImage = resizedImage.copy()
    comparableImage = comparableImage.resize(size)
    comparableImage.save("%s/%s" % (dir, "compareImage.jpg"))

    toCopy = resizedImage.copy()
    count = 1000
    
    for i in range(count):
        if i > 0:
            toCopy = Image.open(newLocation)

        newLocation = "%s/%s.jpg" % (dir, i)
        toCopy = alterImage(toCopy)
        toCopy.save("%s" % (newLocation))

        print "copying image %s" % (i)

        if (i == 0 or (i % 100 == 0)):
            pass
        else:
            oldLocation = "%s/%s.jpg" % (dir, i-1)
            os.remove(oldLocation)

    finalImage = Image.open(newLocation)
    finalImage = finalImage.resize(size)
    finalImage.save("%s/%s-%s" % (dir, count, "finalImage.jpg"))

def alterImage(image):
    x = randint(0,(image.size[0]-1))
    y = randint(0,(image.size[1]-1))
    red = randint(0, 255)
    green = randint(0, 255)
    blue = randint(0, 255)

    print "Changing pixel (%s, %s) to (%s, %s, %s)" % (x, y, red, green, blue)

    image.putpixel((x,y), (red,green,blue))

    return image

def imageToString():
    dir = "/home/k-dazzle/Documents/Programming/Lossifize/copies"
    original = "%s/%s" % (dir, "Refinery.jpg")

    originalImage = Image.open(original)
    print originalImage.tostring()

def imageFromString():
    saveDir = "/home/k-dazzle/Documents/Programming/Lossifize/copies"
    bookDir = "/home/k-dazzle/Documents/nietzsche"
    size = (800, 600)

    niet = open("/home/k-dazzle/Documents/nietzsche/BeyondGoodAndEvil.txt")
    goodAndEvilText = niet.read()
    niet.close()
    niet = open("%s/ThusSpakeZarathustra.txt" % (bookDir))
    zarathustraText = niet.read()
    niet.close()

    goodAndEvil = Image.fromstring("RGBA", (250, 250), goodAndEvilText)
    goodAndEvil.save("%s/BeyondGoodAndEvil-RGBA-2.jpg" % (saveDir))
    larger = goodAndEvil.resize(size)
    larger.save("%s/BeyondGoodAndEvil-RGBigA-2.jpg" % (saveDir))

    zarathustra = Image.fromstring("RGBA", (250, 250), zarathustraText)
    zarathustra.save("%s/ThusSpakeZarathustra-RGBA-2.jpg" % (saveDir))
    largerzar = zarathustra.resize(size)
    largerzar.save("%s/ThusSpakeZarathustra-RGBigA-2.jpg" % (saveDir))

    maskImage1 = Image.open("%s/ThusSpakeZarathustra-RGBigA.png" % (saveDir))
    maskImage2 = Image.open("%s/Refinery.jpg" % (saveDir))
    maskImage2 = maskImage2.resize(size)
    
    compositeImage = Image.composite(largerzar, larger, maskImage1)
    compositeImage.save("%s/composite1A.jpg" % (saveDir))
    compositeImage2 = Image.composite(largerzar, maskImage2, maskImage1)
    compositeImage2.save("%s/composite1A.jpg" % (saveDir))

    comComImage = Image.composite(compositeImage2, larger, maskImage1)
    comComImage.save("%s/composite2.jpg" % (saveDir))

    imageBlend = Image.blend(largerzar, comComImage, .5)
    imageBlend.save("%s/blend3.jpg" % (saveDir))

if __name__ == "__main__":
    # main()
    imageFromString()