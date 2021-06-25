import pygame
import numpy as np
import colorsys
from numba import jit

@jit(nopython=True)
def make_rectangle(p1, p2):
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
        deltax = realfac-xdif # change to x to get 1.5 height

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
        deltay = realfac-ydif # change to y to get height = length / 1.5

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


@jit(nopython=True)
def calculate(x):
    """
    Receive complex number x, return number of iterations
    that the function stays below 2.
    """
    z = 0
    iterations = 0
    while abs(z) <= 2 and iterations < max_iterations:
        z = z**2 + x
        iterations += 1
    return iterations


def plot(reStart, reEnd, imStart, imEnd):
    """
    Plot the colour for each pixel based on iterations
    """
    pixel_x = np.linspace(reStart, reEnd, w)
    pixel_y = np.linspace(imStart, imEnd, h)

    # experimenting with 2 different colour sections added together, e.g. a range of blues and a range of yellows
    #hue1 = np.linspace(186, 90, int(max_iterations/2))
    #hue2 = np.linspace(0, 255, int(max_iterations/2) + 1)
    #hue_range = np.concatenate((hue1, hue2))

    # kind of blue to purple range - my favourite range so far
    hue_range = np.linspace(145, 240, max_iterations+1)
    # experimenting with value and sat ranges, but they don't look as vibrant
    #value_range = np.linspace(50, 255, max_iterations)
    #saturation_range = np.linspace(50, 255, max_iterations+1)
    for i in range(w):
        for j in range(h):
            c = complex(pixel_x[i], pixel_y[j])
            n = calculate(c)
            hue = int(hue_range[n]) # assign hue from linspace index
            #hue = int(n * 130 / max_iterations) # full rgb spectrum

            saturation = 255
            #saturation = 171
            #saturation = int(saturation_range[n])

            if n < max_iterations:
                #value = int(value_range[n])
                value = 255
            else:
                value = 0
            complex_matrix[i][j] = c

            rgb = colorsys.hsv_to_rgb(hue/255, saturation/255, value/255)
            r,g,b = (int(x*255) for x in rgb)
            screen.set_at((i, j), (r, g, b))


def zoom(rect_start, rect_end):
    """
    Receive coordinates drawn on screen, zoom in on those coordinates
    as a rectangle.
    """
    x1 = rect_start[0]
    y1 = rect_start[1]
    x2 = rect_end[0]
    y2 = rect_end[1]
    Re1 = complex_matrix[x1][y1].real
    Im1 = complex_matrix[x1][y1].imag
    Re2 = complex_matrix[x2][y2].real
    Im2 = complex_matrix[x2][y2].imag
    return plot(Re1, Re2, Im1, Im2)


# Setting up initial stuff
pygame.init()
screen = pygame.display.set_mode((800, 600))
w, h = pygame.display.get_surface().get_size()
screen.fill((255, 255, 255))
pygame.display.set_caption('The Mandelbrot Set')

complex_matrix = np.zeros((w, h), dtype=complex) # don't touch this one its so important
max_iterations = 100 # higher = better detail, but more intensive

# range of x and y values to plot
x_start = -2
x_end = 1
y_start = -1
y_end = 1

plot(x_start, x_end, y_start, y_end) # inital mandelbrot plot
pygame.display.update()
rect_start = ()
rect_end = ()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # end program if window is closed
            running = False
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # if mouse button is pressed get the position
            rect_start = event.pos
            pygame.display.update()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: # if mouse button is released get position and zoom in
            rect_end = event.pos
            rect_s, rect_e = make_rectangle(rect_start, rect_end)
            zoom(rect_s, rect_e)
            pygame.display.update()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE: # if backspace is pressed, zoom out fully
                plot(x_start, x_end, y_start, y_end)
                pygame.display.update()
            elif event.key == pygame.K_ESCAPE: # if escape is pressed end program
                pygame.quit()

    print(rect_start, rect_end)
