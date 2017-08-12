#!/usr/bin/env python
from __future__ import print_function
import numpy as np
import random
from PIL import Image

def throw(msg):
    raise RuntimeError(msg)

def neighbors_fn(xy, WIDTH, HEIGHT):
    ret = []
    (x, y) = xy
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if not (dx == 0 and dy == 0):
                nx, ny = x + dx, y + dy
                if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                    ret.append((nx,ny))
    return ret

def coldiff(c1, c2):
    r = c1[0] - c2[0]
    g = c1[1] - c2[1]
    b = c1[2] - c2[2]
    res = (r * r) + (g * g) + (b * b)
    # print("@@@ coldiff", c1, c2, res, "-",r, g, b,
    #       "-", type(r*r), g*g, b*b, "-", (r * r) + (g * g) + (b * b))
    return res

def calcdiff(xy, c, i, pixels, pixels_filled, neighbors):
    diffs = []
    # print("xy", xy, "neighbors", neighbors[xy])
    for n in neighbors[xy]:
        if pixels_filled[n[1], n[0]]:
            c2 = pixels[n[1], n[0]]
            d = coldiff(c, c2)
            diffs.append(d)
            # print("@@@   --diff", n, d, "\t", c, c2)
        else:
            pass
            # print("skipping n", n)
    if len(diffs) == 0:
        print("xy", xy)
        throw('no neighboring spots with paint')
    r = min(diffs)
    # print("@@@ calcdiff", xy, r)
    return r

def main():
    # WIDTH, HEIGHT = 512 * 2, 512 * 4
    # WIDTH, HEIGHT = 256, 128
    # WIDTH, HEIGHT = 4, 2
    WIDTH, HEIGHT = 8, 8
    # WIDTH, HEIGHT = 27, 27
    NUMPIXELS = WIDTH * HEIGHT
    NUMCOLORS = 0
    for guess in xrange(1000):
        g2 = guess ** 3
        if g2 == NUMPIXELS:
            NUMCOLORS = guess
    if NUMCOLORS <= 0:
        throw("illegal image size")
    # @@@
    # STARTX, STARTY = WIDTH / 2, HEIGHT / 2
    STARTX = 0
    STARTY = 0

    # print settings
    print("settings:")
    print("NUMCOLORS", NUMCOLORS)
    print("WIDTH", WIDTH)
    print("HEIGHT", HEIGHT)
    print("STARTX", STARTX)
    print("STARTY", STARTY)

    print("setup")
    # def x(c1, c2):
    #     print("@@@", c1,c2,coldiff(c1,c2))
    # x((75,75,75), (65,65,65))
    # x((75,75,75), (70,70,70))

    # all possible colors
    colors = np.zeros((NUMPIXELS, 3), dtype=np.uint16)
    i = 0
    for r in xrange(NUMCOLORS):
        for g in xrange(NUMCOLORS):
            for b in xrange(NUMCOLORS):
                shift = lambda v: (v * 255) / NUMCOLORS
                colors[i] = (shift(r), shift(g), shift(b))
                i += 1
    # colors = colors[np.random.permutation(len(colors))]
    for i in range(30):
        x = 50 + i * 5
        colors[i] = (x,x,x)
    print("computed colors")
    # print("@@@ colors", colors)

    # 2d array of (r,g,b)
    # each color element is in [0,255]
    pixels = np.zeros((HEIGHT,WIDTH,3), dtype=np.uint16)
    pixels_filled = np.zeros((HEIGHT,WIDTH,1), dtype=np.uint16)

    positions_all = tuple((x, y) for x in xrange(WIDTH) for y in xrange(HEIGHT))

    # map (x, y) => set(neighbor (x, y), ...)
    neighbors = {xy: set(neighbors_fn(xy, WIDTH, HEIGHT)) for xy in positions_all}
    print("computed neighbors")

    # neighbors that have not been painted
    neighbors_empty = {xy: set(neighbors_fn(xy, WIDTH, HEIGHT)) for xy in positions_all}
    print("computed neighbors (2)")

    # list of (x,y) that have not been painted
    # available = np.zeros((0,2), dtype=np.uint32)
    available = set()

    # checkpoints = {(i * len(colors) / 10 - 1): (i - 1) for i in range(11)}
    checkpoints = {i: i for i in range(9)}
    # print("checkpoints", checkpoints)

    print("loop start")

    for i, c in enumerate(colors):
        # c is the color to place

        if i % 4096 == 0:
            print("progress: {}  frontier:{}".format(i / float(NUMPIXELS), len(available)))

        bestxy = None
        if len(available) == 0:
            bestxy = (STARTX, STARTY)
        else:
            bestxy = min(available, key=lambda xy: calcdiff(
                xy, c, i, pixels, pixels_filled, neighbors))

            # bestxy = iter(available).next()

            # bestxy = iter(available).next()
            # bestdiff = 0
            # for xy in available:
            #     diff = 0
            #     if diff < bestdiff:
            #         bestdiff = diff
            #         bestxy = xy

        # print("@@@ {} {}".format(i, bestxy))
        # print("@@@ {} {}".format(i, available))

        # paint the pixel
        pixels[bestxy[1], bestxy[0]] = c
        pixels_filled[bestxy[1], bestxy[0]] = 1
        print(i, "painted", bestxy, pixels[bestxy[1], bestxy[0]])
        # update the empty neighbor cache
        for n in neighbors[bestxy]:
            neighbors_empty[n].discard(bestxy)

        # add the neighbors
        available.update(neighbors_empty[bestxy])
        # delete bestxy from the available set
        available.discard(bestxy)

        # if i % 4096 == 0:
        #     filename = "result{}.png".format(i)
        #     print("checkpoint", filename)
        #     Image.fromarray(pixels, 'RGB').save(filename)
        if i in checkpoints:
            filename = "result{}.png".format(checkpoints[i])
            print("checkpoint", filename)
            Image.fromarray(pixels, 'RGB').save(filename)

    Image.fromarray(pixels, 'RGB').save("resultZ.png".format(i))

    print("done")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
