from Tkinter import *
import os
from PIL import Image
import ctypes
from PIL import ImageTk
from PIL import ImageOps
from tkFileDialog import *
import tkMessageBox
import imghdr
from PIL import ImageDraw
from collections import *



def blur(canvas):       #equalizer(Changing color)
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    if canvas.data.image != None:
        canvas.data.image = ImageOps.equalize(canvas.data.image,  mask=None)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)


def second(canvas):        #Black and White
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    if canvas.data.image != None:
        canvas.data.image = ImageOps.grayscale(canvas.data.image)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)


def fourth(canvas):     #Border
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    if canvas.data.image != None:
        canvas.data.image = ImageOps.expand(canvas.data.image,border=9,fill="black")
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)


def fifth(canvas):     #Mirror Effect
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    if canvas.data.image != None:
        canvas.data.image = ImageOps.mirror(canvas.data.image)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)


def last(canvas):     #Flip_Effect
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    if canvas.data.image != None:
        canvas.data.image = ImageOps.flip(canvas.data.image)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)


def reset(canvas):      ### change back to original image
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    if canvas.data.image != None:
        canvas.data.image = canvas.data.originalImage.copy()
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)


def brightness(canvas):     #Brightness
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.drawOn = False
    brightnessWindow = Toplevel(canvas.data.mainWindow)
    brightnessWindow.title("Brightness")
    brightnessSlider = Scale(brightnessWindow, from_=-100, to=100, \
                             orient=HORIZONTAL)
    brightnessSlider.pack()
    OkBrightnessFrame = Frame(brightnessWindow)
    OkBrightnessButton = Button(OkBrightnessFrame, text="OK", \
                                command=lambda: closeBrightnessWindow(canvas))
    OkBrightnessButton.grid(row=0, column=0)
    OkBrightnessFrame.pack(side=BOTTOM)
    changeBrightness(canvas, brightnessWindow, brightnessSlider, 0)
    brightnessSlider.set(0)

def closeBrightnessWindow(canvas):
    if canvas.data.image != None:
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.brightnessWindowClose = True


def changeBrightness(canvas, brightnessWindow, brightnessSlider, \
                     previousVal):
    if canvas.data.brightnessWindowClose == True:
        brightnessWindow.destroy()
        canvas.data.brightnessWindowClose = False

    else:
        # increasing pixel values according to slider value increases
        # brightness we change ot according to the difference between the
        # previous value and the current slider value
        if canvas.data.image != None and brightnessWindow.winfo_exists():
            sliderVal = brightnessSlider.get()
            scale = (sliderVal - previousVal) / 100.0
            canvas.data.image = canvas.data.image.point( \
                lambda i: i + int(round(i * scale)))
            canvas.data.imageForTk = makeImageForTk(canvas)
            drawImage(canvas)
            canvas.after(200, \
                         lambda: changeBrightness(canvas, brightnessWindow, \
                                                  brightnessSlider, sliderVal))


def dummy(canvas):
    x =0


# MENU COMMANDS #

def saveAs(canvas):
    # ask where the user wants to save the file
    if canvas.data.image != None:
        filename = asksaveasfilename(defaultextension=".jpg")
        im = canvas.data.image
        im.save(filename)


def save(canvas):
    if canvas.data.image != None:
        im = canvas.data.image
        im.save(canvas.data.imageLocation)


def newImage(canvas):
    imageName = askopenfilename()
    filetype = ""
    try:
        filetype = imghdr.what(imageName)
    except:
        tkMessageBox.showinfo(title="Image File", \
                              message="Choose an Image File!", parent=canvas.data.mainWindow)
    # restrict filetypes to .jpg, .bmp, etc.
    if filetype in ['jpeg', 'bmp', 'png', 'tiff']:
        canvas.data.imageLocation = imageName
        im = Image.open(imageName)
        canvas.data.image = im
        canvas.data.originalImage = im.copy()
        canvas.data.undoQueue.append(im.copy())
        canvas.data.imageSize = im.size  # Original Image dimensions
        canvas.data.imageForTk = makeImageForTk(canvas)
        drawImage(canvas)
    else:
        tkMessageBox.showinfo(title="Image File", \
                              message="Choose an Image File!", parent=canvas.data.mainWindow)


def makeImageForTk(canvas):
    im = canvas.data.image
    if canvas.data.image != None:
        imageWidth = canvas.data.image.size[0]
        imageHeight = canvas.data.image.size[1]
        if imageWidth > imageHeight:
            resizedImage = im.resize((canvas.data.width, \
                                      int(round(float(imageHeight) * canvas.data.width / imageWidth))))

            canvas.data.imageScale = float(imageWidth) / canvas.data.width
        else:
            resizedImage = im.resize((int(round(float(imageWidth) * canvas.data.height / imageHeight)), \
                                      canvas.data.height))
            canvas.data.imageScale = float(imageHeight) / canvas.data.height
        canvas.data.resizedIm = resizedImage
        return ImageTk.PhotoImage(resizedImage)


def drawImage(canvas):
    if canvas.data.image != None:
        # make the canvas center and the image center the same
        canvas.create_image(canvas.data.width / 2.0 - canvas.data.resizedIm.size[0] / 2.0,
                            canvas.data.height / 2.0 - canvas.data.resizedIm.size[1] / 2.0,
                            anchor=NW, image=canvas.data.imageForTk)
        canvas.data.imageTopX = int(round(canvas.data.width / 2.0 - canvas.data.resizedIm.size[0] / 2.0))
        canvas.data.imageTopY = int(round(canvas.data.height / 2.0 - canvas.data.resizedIm.size[1] / 2.0))



# INITIALIZE #

def init(root, canvas):
    menuInit(root, canvas)
    canvas.data.image = None
    canvas.data.angleSelected = None
    canvas.data.rotateWindowClose = False
    canvas.data.brightnessWindowClose = False
    canvas.data.brightnessLevel = None
    canvas.data.histWindowClose = False
    canvas.data.solarizeWindowClose = False
    canvas.data.posterizeWindowClose = False
    canvas.data.colourPopToHappen = False
    canvas.data.cropPopToHappen = False
    canvas.data.endCrop = False
    canvas.data.drawOn = True
    canvas.data.undoQueue = deque([], 10)
    canvas.data.redoQueue = deque([], 10)
    canvas.pack()


def menuInit(root, canvas):
    menubar = Menu(root)
    menubar.add_command(label="    ", command=lambda: dummy(canvas))
    menubar.add_command(label="Choose Image", command=lambda: newImage(canvas))
    menubar.add_command(label="                          ", command=lambda: dummy(canvas))

    menubar.add_command(label="Reset Image", command=lambda: reset(canvas))
    menubar.add_command(label="                          ", command=lambda: dummy(canvas))

    menubar.add_command(label="Save Image", command=lambda: saveAs(canvas))

    menubar.add_command(label="Equalizer", command=lambda: blur(canvas))
    menubar.add_command(label="    ", command=lambda: dummy(canvas))


    menubar.add_command(label="Grayscale", command=lambda: second(canvas))
    menubar.add_command(label="    ", command=lambda: dummy(canvas))

    menubar.add_command(label="Add_Border", command=lambda: fourth(canvas))
    menubar.add_command(label="    ", command=lambda: dummy(canvas))


    menubar.add_command(label="Mirror", command=lambda: fifth(canvas))
    menubar.add_command(label="    ", command=lambda: dummy(canvas))


    menubar.add_command(label="Brightness", command=lambda: brightness(canvas))
    menubar.add_command(label="    ", command=lambda: dummy(canvas))


    menubar.add_command(label="Fliping", command=lambda: last(canvas))
    root.config(menu=menubar)


def run():
    # create the root and the canvas
    root = Tk()
    root.title("Image Editor")
    canvasWidth = 550
    canvasHeight = 400
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight, \
                    background="white")

    # Set up canvas data and call init
    class Struct: pass

    canvas.data = Struct()
    canvas.data.width = canvasWidth
    canvas.data.height = canvasHeight
    canvas.data.mainWindow = root
    init(root, canvas)
    root.bind("<Key>", lambda event: keyPressed(canvas, event))
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits)


run()