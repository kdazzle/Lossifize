import sys
import glob, os
import getopt
from shutil import copy
import random
from random import randint
from PIL import Image


__author__="Kyle Valade"
__date__ ="$11-Dec-2011 4:32:20 PM$"

def main(argv=None):
    inputFile = None
    help = None
    copies = None
    directory = None

    argList = {'file': inputFile, 'copies': copies, 'directory': directory}

    try:
        opts, args = getopt.getopt(sys.argv[1:], "fct:h", ["file=", "help=",
        "copies=", "targetDirectory"])
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                help = getHelpText()
                print help
            elif opt in ("-f", "--file"):
                argList['file'] = arg
                print "File: ", inputFile
            elif opt in ("-c", "--copies"):
                argList['copies'] = int(arg)
                print "Copies: ", copies
            elif opt in ("-t", "--targetDirectory"):
                argList['directory'] = arg
            else:
                print "Incorrect arguments, -h for help."

    except getopt.GetoptError:
        sys.exit(2)

    if not argList['file'] and not help:
        print "You need to enter a file"
    if not argList['copies'] and not help:
        print "How many copies do you want?"
    if argList['file'] and argList['copies']:
        lossifize(argList, outputDir)

def getHelpText():
    help ="""
    --copies            -c  (required)  the amount of copies that you want to make - at
                            least 30,000 is recommended
    --file              -f  (required) the file that you are trying to copy
    --help              -h  help
    --targetDirectory   -t  (required) the directory you are saving to

    Files will be saved into the copies folder in the Lossifize directory
    """

    return help

def lossifize(argList, targetDir):
    inputFile = argList['file']
    copies = argList['copies']
    targetDir = argList['dir']

    originalImage = Image.open(inputFile)

    size = originalImage.size
    newWidth = size[0] / 2
    newHeight = size[1] / 2

    resizedImage = originalImage.copy()
    resizedImage = resizedImage.resize((newWidth, newHeight))
    resizedImage.save("%s/%s" % (targetDir, "resized.jpg"))


    comparableImage = resizedImage.copy()
    comparableImage = comparableImage.resize(size)
    comparableImage.save("%s/%s" % (targetDir, "compareImage.jpg"))

    toCopy = resizedImage.copy()
    count = copies

    for i in range(count):
        if i > 0:
            toCopy = Image.open(newLocation)

        newLocation = "%s/%s.jpg" % (targetDir, i)
        toCopy = alterImage(toCopy)
        toCopy.save("%s" % (newLocation))

        print "copying image %s" % (i)

        if (i == 0 or (i % 100 == 0)):
            pass
        else:
            oldLocation = "%s/%s.jpg" % (targetDir, i-1)
            os.remove(oldLocation)

    finalImage = Image.open(newLocation)
    finalImage = finalImage.resize(size)
    finalImage.save("%s/%s-%s" % (targetDir, count, "finalImage.jpg"))

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
    main(sys.argv[1:])
