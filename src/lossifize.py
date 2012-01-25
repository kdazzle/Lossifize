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
    targetDirectory = "../copies"
    saveIncrement = 100


    argList = {'file': inputFile, 'copies': copies, 'targetDirectory': targetDirectory,
                'saveIncrement': saveIncrement}

    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:c:t:i:h", ["file=", "copies=",
            "help"])
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                help = getHelpText()
                print help
            elif opt in ("-f", "--file"):
                argList['file'] = arg
                print "File: %s" % (arg)
            elif opt in ("-c", "--copies"):
                argList['copies'] = int(arg)
                print "Copies: %s" % arg
            elif opt in ("-t"):
                argList['targetDirectory'] = arg
                print "Directory: %s" % (arg)
            elif opt in ("-i"):
                argList['saveIncrement'] = int(arg)
            else:
                print "Incorrect arguments, -h for help."

    except getopt.GetoptError:
        sys.exit(2)

    if not help:
        if not argList['file']:
            print "You need to enter a file -h for help"
        if not argList['copies']:
            print "How many copies do you want? -h for help"

    if argList['file'] and argList['copies']:
        lossifize(argList)

def getHelpText():
    help ="""
    -c    --copies          (required)  the amount of copies that you want to
                                make - at least 30,000 is recommended
    -f    --file            (required) the file that you are trying to copy
    -h                      Show this stuff
    -i    Save Increment    the increments to save files at. Eg: to save every
                                thousandth picture, use -i 1000. Default is 100
    -t                      the directory you are saving to. Defaults to ./copies
    """

    return help

def lossifize(argList):
    """This function could definitely use some cleaning up"""

    inputFile = argList['file']
    copies = argList['copies']
    targetDir = argList['targetDirectory']
    saveIncrement = argList['saveIncrement']

    originalImage = Image.open(inputFile)

    originalSize = originalImage.size

    # resize to increase eventual image loss...? Possibly unnecessary.
    newWidth = originalSize[0] / 2
    newHeight = originalSize[1] / 2

    resizedImage = originalImage.copy()
    resizedImage = resizedImage.resize((newWidth, newHeight))
    resizedImage.save("%s/%s" % (targetDir, "resized.jpg"))

    # create a halfsize image for comparing later images
    comparableImage = resizedImage.copy()
    comparableImage = comparableImage.resize(originalSize)
    comparableImage.save("%s/%s" % (targetDir, "compareImage.jpg"))

    imageToCopy = resizedImage.copy()
    count = copies

    for i in range(count):
        if i > 0:
            imageToCopy = Image.open(newLocation)

        newLocation = "%s/%s.jpg" % (targetDir, i)
        imageToCopy = insertRandomPixel(imageToCopy)
        imageToCopy.save("%s" % (newLocation))

        if (i == 0 or (i % saveIncrement == 0)):
            pass
        else:
            oldLocation = "%s/%s.jpg" % (targetDir, i-1)
            os.remove(oldLocation)

    finalImage = Image.open(newLocation)
    finalImage = finalImage.resize(originalSize)
    finalImage.save("%s/%s-%s" % (targetDir, count, "finalImage.jpg"))

def insertRandomPixel(image):
    """Inserts a random pixel into the image in order to break up the jpeg
    compression and eventually encourage errors. Certainly doesn't have to
    be done every iteration."""
    
    x = randint(0,(image.size[0]-1))
    y = randint(0,(image.size[1]-1))

    # setting the upper values to 999 was actually kind of interesting, too
    red = randint(0, 255)
    green = randint(0, 255)
    blue = randint(0, 255)

    # uncomment this if you want the program to run even slower
    # or if you want to see a record of the pixel changes
    #print "Changing pixel (%s, %s) to (%s, %s, %s)" % (x, y, red, green, blue)

    image.putpixel((x,y), (red,green,blue))

    return image

if __name__ == "__main__":
    main(sys.argv[1:])
