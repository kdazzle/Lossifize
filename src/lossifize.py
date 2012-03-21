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
    saveIncrement = None


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
    help = """
    -c    --copies          (required)  the amount of copies that you want to
                                make - at least 30,000 is recommended
    -f    --file            (required) the file that you are trying to copy
    -h                      Show this stuff
    -i    Save Increment    the increments to save files at. Eg: to save every
                                thousandth picture, use -i 1000. Default is 10%
    -t                      the directory you are saving to. Defaults to ./copies


	To call the program, do something like this:
	  python ./lossifize.py -f /path/to/file -c 30000
    """

    return help

def lossifize(argList):
    """This function could definitely use some cleaning up"""

    inputFile = argList['file']
    copies = argList['copies']
    targetDir = argList['targetDirectory']
    saveIncrement = getSaveIncrement(argList)

    originalImage = Image.open(inputFile)
    originalSize = originalImage.size

    smallerImage = createSmallerImage(originalImage, targetDir)

    # immediately return the smaller image to its original size -
    #   to give a control to the experiment
    comparableImageFilepath = "%s/%s" % (targetDir, "compareImage.jpg")
    copyImage(smallerImage, comparableImageFilepath, originalSize)

    penultimateImagepath = performCopying(copies, saveIncrement, smallerImage, targetDir)

    saveFinalImage(penultimateImagepath, originalSize, targetDir, copies)

def getSaveIncrement(argList):
    """Calculates the saveIncrement. Defaults to 10%. Returns an integer"""

    saveIncrement = argList['saveIncrement']

    if (saveIncrement == None):
        copies = argList['copies']
        saveIncrement = copies / 10

    return saveIncrement

def createSmallerImage(originalImage, targetDir):
    """create an image that's half the size. This increases loss when it's resized later"""

    originalSize = originalImage.size
    smallerImageFilepath = "%s/%s" % (targetDir, "resized.jpg")
    smallerDimensions = getSmallerDimensions(originalSize)
    return copyImage(originalImage, smallerImageFilepath, smallerDimensions)

def getSmallerDimensions(originalSize):
    """Returns a tuple of (width, height). This is done to increase the lossiness
    of the image when we return the image to its original size."""

    newWidth = originalSize[0] / 2
    newHeight = originalSize[1] / 2

    return (newWidth, newHeight)

def copyImage(originalImage, targetPath, dimensions = None):
    """Copies an image, saves it to the given filepath. Also resizes the image
    if dimensions is specified. The copied image is returned."""

    copiedImage = originalImage.copy()

    if (not dimensions == None):
        copiedImage = copiedImage.resize(dimensions)
        
    copiedImage.save(targetPath)

    return copiedImage

def performCopying(copies, saveIncrement, smallerImage, targetDir):
    """This is the function that does most of the work - makes all of the copies
    of the image. Returns the location of the penultimate image."""
    
    imageToCopy = smallerImage.copy()
    count = copies + 1

    for i in xrange(1, count):
        if i > 1:
            imageToCopy = Image.open(currentFilepath)

        currentFilepath = "%s/%s.jpg" % (targetDir, i)
        imageToCopy = insertRandomPixel(imageToCopy)
        imageToCopy.save("%s" % currentFilepath)

        # Don't delete the first image or an image at the specified increment
        if (i == 1 or (i % saveIncrement == 0)):
            print "saving image %s" % (i)
        else:
            # otherwise, delete the previous image
            oldLocation = "%s/%s.jpg" % (targetDir, i-1)
            os.remove(oldLocation)

    return currentFilepath

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

def saveFinalImage(imageLocation, originalSize, targetDir, count):
    finalImage = Image.open(imageLocation)
    finalImage = finalImage.resize(originalSize)
    finalImage.save("%s/%s-%s" % (targetDir, count, "finalImage.jpg"))

if __name__ == "__main__":
    main(sys.argv[1:])
