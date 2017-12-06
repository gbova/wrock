#pygletTest.py

#! /usr/bin/env python

import sys
import threading
from threading import Thread
import pyglet
from pyglet import media

player = pyglet.media.Player()
playerLock = threading.Lock()

IOLock = threading.Lock()


def queueSound(aSound):
    pointlessVar = 0
    for i in range (0, 100):
        for j in range (0, 100):
            pointlessVar += 1
    IOLock.acquire()
    print("playing my sound")
    IOLock.release()
    playerLock.acquire()
    player.queue(aSound)
    playerLock.release()

def main(argv):
    #window = pyglet.window.Window()
    explosion = pyglet.media.load('explosion.wav', streaming=False)
    lion = pyglet.media.load('lion2.wav', streaming=False)
    boing = pyglet.media.load('boing_x.wav', streaming=False)
    cymbals = pyglet.media.load('cymbals.wav', streaming=False)
    bubbles = pyglet.media.load('bubbles_sfx.wav', streaming=False)
    cuckoo = pyglet.media.load('cuckoo_clock1_x.wav', streaming=False)


    sounds = [explosion, lion, boing, cymbals, bubbles, cuckoo]

    threads = []
    numThreads = 25
    for i in range (0,numThreads):
        newThr = Thread(target=queueSound, args=(sounds[i%6],))
        threads.append(newThr)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    player.play()
    pyglet.app.run()


if __name__ == '__main__':
    main(sys.argv)
