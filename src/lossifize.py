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

if __name__ == "__main__":
    main()