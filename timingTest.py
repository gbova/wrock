#timingTest.py
#! /usr/bin/env python

import sys
import threading
from threading import Thread
import pyglet
from pyglet import media

players = []
playerLock = threading.Lock()

explosion = pyglet.media.load('soundEffects/explosion.wav', streaming=False)
lion = pyglet.media.load('soundEffects/lion2.wav', streaming=False)
boing = pyglet.media.load('soundEffects/boing_x.wav', streaming=False)
cymbals = pyglet.media.load('soundEffects/cymbals.wav', streaming=False)
bubbles = pyglet.media.load('soundEffects/bubbles_sfx.wav', streaming=False)
cuckoo = pyglet.media.load('soundEffects/cuckoo_clock1_x.wav', streaming=False)
hp1 = pyglet.media.load('hp_music/harry_potter.wav', streaming=False)
hp2 = pyglet.media.load('hp_music/harry_potter-2.wav', streaming=False)
hogwarts = pyglet.media.load('hp_music/happy_hogwarts.wav', streaming=False)
christmas = pyglet.media.load('hp_music/hogwarts_christmas.wav', streaming=False)
laugh = pyglet.media.load('hp_music/voldemort_laugh.wav', streaming=False)

sounds1 = [explosion, lion, boing, cymbals, bubbles, cuckoo]
sounds2 = [hp1, hp2, hogwarts, christmas, laugh, laugh]

def playMusic(num):
    newplayer = pyglet.media.Player()
    newplayer.queue(sounds2[num])
    playerLock.acquire()
    players.append(newplayer)
    playerLock.release()

def exit_callback(dt):
    pyglet.app.exit()

def main(argv):
    threads = []
    for x in range (0, 6):
        newThr = Thread(target=playMusic, args=(x,))
        threads.append(newThr)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    pgroup = pyglet.media.PlayerGroup(players)
    pgroup.play()
    pyglet.clock.schedule_once(exit_callback, 10)
    pyglet.app.run()


if __name__ == '__main__':
    main(sys.argv)
