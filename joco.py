#!/usr/bin/env python
from __future__ import print_function
import numpy as np
from PIL import Image

def throw(msg):
    raise RuntimeError(msg)

def neighbors(xy, WIDTH, HEIGHT, pixels):
    ret = []
    (x, y) = xy
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if not (dx == 0 and dy == 0):
                nx, ny = x + dx, y + dy
                if nx < WIDTH and ny < HEIGHT and pixels[ny, nx].sum() == 0:
                    ret.append((nx,ny))
    return ret

def main():
    WIDTH = 256
    HEIGHT = 128
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

    # 2d array of (r,g,b)
    # each color element is in [0,255]
    pixels = np.zeros((HEIGHT,WIDTH,3), dtype=np.uint8)

    # list of (x,y)
    # available = np.zeros((0,2), dtype=np.uint32)
    available = set()

    colors = np.zeros((NUMPIXELS, 3), dtype=np.uint8)
    i = 0
    for r in xrange(NUMCOLORS):
        for g in xrange(NUMCOLORS):
            for b in xrange(NUMCOLORS):
                shift = lambda v: (v * 255) / NUMCOLORS
                colors[i] = (shift(r), shift(g), shift(b))
                i += 1
    np.random.shuffle(colors)

    print("loop start")

    for i, c in enumerate(colors):
        # c is the color to place

        if i % 1024 == 0:
            print("progress: {}  queue:{}".format(i / float(NUMPIXELS), len(available)))

        bestxy = None
        if len(available) == 0:
            bestxy = (STARTX, STARTY)
        else:
            # scores = available
            # bestxy = available[scores.argmin()]
            # bestxy = available[0]
            bestxy = iter(available).next()

        # print("@@@ {} {}".format(i, bestxy))
        # print("@@@ {} {}".format(i, available))

        pixels[bestxy[1], bestxy[0]] = c

        # # add the neighbors
        # # can add duplicates, but the above delete will catch them in future sweeps
        # available = np.append(available, neighbors(bestxy, WIDTH, HEIGHT), axis=0)
        # # delete bestxy from the available list
        # to_delete = []
        # for j, xy in enumerate(available):
        #     if xy[0] == bestxy[0] and xy[1] == bestxy[1]:
        #         to_delete.append(j)
        # if i > 0 and len(to_delete) == 0:
        #     throw("fault in delete from available")
        # available = np.delete(available, to_delete, axis=0)

        # add the neighbors
        available.update(neighbors(bestxy, WIDTH, HEIGHT, pixels))
        # delete bestxy from the available set
        available.discard(bestxy)

        if i % 2048 == 0:
            filename = "result{}.png".format(i)
            print("checkpoint", filename)
            Image.fromarray(pixels, 'RGB').save(filename)

    Image.fromarray(pixels, 'RGB').save("result{}.png".format(i))

    print("done")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
