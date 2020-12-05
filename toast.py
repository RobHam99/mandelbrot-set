import pygame
import numpy as np
import colorsys
#from numba import jit


def makerect(p1, p2):
    """
    Function to make sure the zoom doesn't squish dimensions
    e.g. if you draw a rectangle way longer than it is high
    it will rearrange it into a rectangle where length = 1.5*height
    """

    xdif = p2[0]-p1[0]
    ydif = p2[1]-p1[1]

    if xdif == 1.5*ydif: # if length is 1.5 height return
        return p1, p2

    elif xdif < 1.5*ydif: # if length is less than 1.5 height
        realfac = 1.5*ydif # what length should be
        deltax = realfac-xdif # changed to x to get 1.5 heigh

        # if change will stay in screen coords
        if (p1[0] - (deltax/2)) >= 0 and (p2[0] + (deltax/2)) <= w:
            newx1 = int(p1[0] - (deltax/2))
            newx2 = int(p2[0] + (deltax/2))
            return (newx1, p1[1]), (newx2, p2[1])

        # if change will go out of screen left
        elif (p1[0] - (deltax/2)) < 0 and (p2[0] + (deltax/2)) <= w:
            for i in range(w):
                if (p1[0] - (deltax/2) + i) >= 0:
                    newx1 = int((p1[0] - (deltax/2) + i))
                    deltax1 = p1[0] - newx1
                    newx2 = int((p2[0] + (deltax - deltax1)))
                    return (newx1, p1[1]), (newx2, p2[1])

        # if change will go out of screen right
        elif (p1[0] - (deltax/2)) >= 0 and (p2[0] + (deltax/2)) > w:
            for i in range(w):
                if (p2[0] + (deltax/2) - i) <= w:
                    newx2 = int((p2[0] + (deltax/2) - i))
                    deltax2 = newx2 - p2[0]
                    newx1 = int(p1[0] - (deltax - deltax2))
                    return (newx1, p1[1]), (newx2, p2[1])

    else: # if length is more than 1.5 height
        realfac = xdif/1.5 # what height should be
        deltay = realfac-ydif

        # if change will stay in screen coords
        if (p1[1] - (deltay/2)) >= 0 and (p2[1] + (deltay/2)) <= h:
            newy1 = int(p1[1] - (deltay/2))
            newy2 = int(p2[1] + (deltay/2))
            return (p1[0], newy1), (p2[0], newy2)

        # if change will go out of screen top
        elif (p1[1] - (deltay/2)) < 0 and (p2[1] + (deltay/2)) <= h:
            for i in range(h):
                if (p1[1] - (deltay/2) + i) >= 0:
                    newy1 = int((p1[1] - (deltay/2) + i))
                    deltay1 = p1[1] - newy1
                    newy2 = int((p2[1] + (deltay - deltay1)))
                    return (p1[0], newy1), (p2[0], newy2)

        # if change will go out of screen bottom
        elif (p1[1] - (deltay/2)) >= 0 and (p2[1] + (deltay/2)) > h:
            for i in range(h):
                if (p2[1] + (deltay/2) - i) <= h:
                    newy2 = int((p2[1] + (deltay/2) - i))
                    deltay2 = newy2 - p2[1]
                    newy1 = int(p1[1] - (deltay - deltay2))
                    return (p1[0], newy1), (p2[0], newy2)



#class mandelbrot:
    #def __init__(self, max_iterations):
        #self.max_iterations = max_iterations
#@jit(nopython=True)
def calculate(x):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iterations:
        z = z*z + x
        n += 1
    return n

def plot(reStart, reEnd, imStart, imEnd):
    pixel_X = np.linspace(reStart, reEnd, w)
    pixel_Y = np.linspace(imStart, imEnd, h)


    for i in range(w):
        for j in range(h):
            cc = complex(pixel_X[i], pixel_Y[j])
            n = calculate(cc)
            hue = int(n * 255 / max_iterations)
            saturation = 255
            if n < max_iterations:
                value = 255
            else:
                value = 0
            complexMatrix[i][j] = cc

            rgb = colorsys.hsv_to_rgb(hue/255, saturation/255, value/255)
            r,g,b = (int(x*255) for x in rgb)
            screen.set_at((i, j), (r, g, b))

    #return #complexMatrix

def zoom(rectStart, rectEnd):
    #plot(reStart, reEnd, imStart, imEnd)
    x1 = rectStart[0]
    y1 = rectStart[1]
    x2 = rectEnd[0]
    y2 = rectEnd[1]
    Re1 = complexMatrix[x1][y1].real
    Im1 = complexMatrix[x1][y1].imag
    Re2 = complexMatrix[x2][y2].real
    Im2 = complexMatrix[x2][y2].imag

    return plot(Re1, Re2, Im1, Im2)

# Setting up initial stuff
pygame.init()
screen = pygame.display.set_mode((800, 600))
w, h = pygame.display.get_surface().get_size()
screen.fill((255, 255, 255))
pygame.display.set_caption('The Mandelbrot Set')

complexMatrix = np.zeros((w, h), dtype=complex)
max_iterations = 80
reStart = -2
reEnd = 1
imStart = -1
imEnd = 1

#mand = mandelbrot(max_iterations)
plot(reStart, reEnd, imStart, imEnd)

rectStart = ()
rectEnd = ()
MBD = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            rectStart = event.pos
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            rectEnd = event.pos
            rectS, rectE = makerect(rectStart, rectEnd)
            zoom(rectS, rectE)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                plot(reStart, reEnd, imStart, imEnd)
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()

    pygame.event.get()
    #print(rectStart, rectEnd)
    pygame.display.update()
