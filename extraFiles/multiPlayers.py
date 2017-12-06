#! /usr/bin/env python

import sys
import time
import threading
from threading import Thread
import pyglet
from pyglet import media

boing = pyglet.media.load('soundEffects/boing_x.wav', streaming=False)

def play():
    player = pyglet.media.Player()
    player.queue(boing)
    player.play()

def exit_callback(dt):
    pyglet.app.exit()

def main(argv):
    thread1 = Thread(target=play)
    thread2 = Thread(target=play)
    thread1.start()
    thread2.start()
    pyglet.clock.schedule_once(exit_callback, 5)
    #pyglet.app.run()


if __name__ == '__main__':
    main(sys.argv)
