import pygame
import numpy as np
import colorsys
from numba import jit

#class mandelbrot:
    #def __init__(self, max_iterations):
        #self.max_iterations = max_iterations
@jit(nopython=True)
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
max_iterations = 1000

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
            zoom(rectStart, rectEnd)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                plot(reStart, reEnd, imStart, imEnd)
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()

    pygame.event.get()
    #print(rectStart, rectEnd)
    pygame.display.update()
