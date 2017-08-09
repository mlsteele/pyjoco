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

def main():
    WIDTH = 512 #* 2
    HEIGHT = 512 #* 4
    NUMPIXELS = WIDTH * HEIGHT
    NUMCOLORS = 0
    for guess in xrange(1000):
        g2 = guess ** 3
        if g2 == NUMPIXELS:
            NUMCOLORS = guess
    if NUMCOLORS <= 0:
        throw("illegal image size")
    STARTX = WIDTH / 2
    STARTY = HEIGHT / 2

    # print settings
    print("settings:")
    print("NUMCOLORS", NUMCOLORS)
    print("WIDTH", WIDTH)
    print("HEIGHT", HEIGHT)
    print("STARTX", STARTX)
    print("STARTY", STARTY)

    print("setup")

    # all possible colors
    colors = np.zeros((NUMPIXELS, 3), dtype=np.uint8)
    i = 0
    for r in xrange(NUMCOLORS):
        for g in xrange(NUMCOLORS):
            for b in xrange(NUMCOLORS):
                shift = lambda v: (v * 255) / NUMCOLORS
                colors[i] = (shift(r), shift(g), shift(b))
                i += 1
    colors = colors[np.random.permutation(len(colors))]
    print("computed colors")

    # 2d array of (r,g,b)
    # each color element is in [0,255]
    pixels = np.zeros((HEIGHT,WIDTH,3), dtype=np.uint8)

    positions_all = tuple((x, y) for x in xrange(WIDTH) for y in xrange(HEIGHT))

    # map (x, y) => set(neighbor (x, y), ...)
    neighbors = {xy: set(neighbors_fn(xy, WIDTH, HEIGHT)) for xy in positions_all}
    print("computed neighbors")

    neighbors_empty = neighbors.copy()

    # list of (x,y) that have not been painted
    # available = np.zeros((0,2), dtype=np.uint32)
    available = set()

    checkpoints = {(i * len(colors) / 10 - 1): (i - 1) for i in range(11)}
    print(checkpoints)

    print("loop start")

    for i, c in enumerate(colors):
        # c is the color to place

        if i % 4096 == 0:
            print("progress: {}  queue:{}".format(i / float(NUMPIXELS), len(available)))

        bestxy = None
        if len(available) == 0:
            bestxy = (STARTX, STARTY)
        else:
            bestxy = iter(available).next()

        # print("@@@ {} {}".format(i, bestxy))
        # print("@@@ {} {}".format(i, available))

        # paint the pixel
        pixels[bestxy[1], bestxy[0]] = c
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

    Image.fromarray(pixels, 'RGB').save("result{}.png".format(i))

    print("done")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
