import numpy as np

def makerect(p1, p2):
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


def calculate(x):
    """
    Receive complex number x, return number of iterations
    that the function stays below 2.
    """
    z = 0
    n = 0
    Zvals = np.zeros(max_iterations+1, dtype=complex)
    while abs(z) <= 2 and n < max_iterations:
        z = z*z + x
        n += 1
        Zvals[n] = z
    return n, Zvals

def screen2(number):
    Zvals = calculate(number)[1]
    print(Zvals)
    return Zvals


max_iterations = 10

number = complex(-0.5, 0.5)

Zvals = screen2(number)
