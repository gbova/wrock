#timingTest.py
#! /usr/bin/env python

import sys
import threading
from threading import Thread
import pyglet
from pyglet import media

# music
explosion = pyglet.media.load('soundEffects/explosion.wav', streaming=False)
lion = pyglet.media.load('soundEffects/lion2.wav', streaming=False)
boing = pyglet.media.load('soundEffects/boing_x.wav', streaming=False)
cymbals = pyglet.media.load('soundEffects/cymbals.wav', streaming=False)
bubbles = pyglet.media.load('soundEffects/bubbles_sfx.wav', streaming=False)
cuckoo = pyglet.media.load('soundEffects/cuckoo_clock1_x.wav', streaming=False)

#tones
hp1 = pyglet.media.load('hp_music/harry_potter.wav', streaming=False)
hp2 = pyglet.media.load('hp_music/harry_potter-2.wav', streaming=False)
hogwarts = pyglet.media.load('hp_music/hogwarts_christmas.wav', streaming=False)
christmas = pyglet.media.load('hp_music/hogwarts_christmas.wav', streaming=False)
#characters
voldemort = pyglet.media.load('hp_music/voldemort_laugh.wav', streaming=False)
harry = pyglet.media.load('hp_music/mental.wav', streaming=False) #
hermione = pyglet.media.load('hp_music/mental.wav', streaming=False) #
snape = pyglet.media.load('hp_music/snape_fame.wav', streaming=False)
hagrid = pyglet.media.load('hp_music/youreawizard.wav', streaming=False)
malfoy = pyglet.media.load('hp_music/youreawizard.wav', streaming=False) #
dumbledore = pyglet.media.load('hp_music/snape_fame.wav', streaming=False)
ron = pyglet.media.load('hp_music/mental.wav', streaming=False)

longsilence = pyglet.media.load('hp_music/silence_10.wav', streaming=False)
shortsilence = pyglet.media.load('hp_music/silent.wav', streaming=False)
#sounds1 = [explosion, lion, boing, cymbals, bubbles, cuckoo]
#sounds2 = [hp1, hp2, hogwarts, christmas, laugh, laugh]

# vars, locks, and dicts
players = []
playerLock = threading.Lock()

PTable = []
chars1 = ["Harry", "Ron", "Hermione", "Malfoy"]
chars2 = ["Voldemort", "Hagrid", "Dumbledore", "Snape"]
allChars = chars1 + chars2
tones = ["joy", "exciting", "tentative", "neutral"]
musicDict = {"joy": christmas, "neutral" : hogwarts, "tentative" : hp1,
             "exciting" : hp2, "Voldemort" : voldemort, "Harry" : harry,
             "Ron" : ron, "Hermione" : hermione, "Malfoy" : malfoy,
             "Dumbledore" : dumbledore, "Hagrid" : hagrid, "Snape" : snape}

#def playMusic(num):
#    newplayer = pyglet.media.Player()
#    for x in range (0, 5):
#        newplayer.queue(sounds2[num])
#        newplayer.queue(silence)
#        newplayer.queue(silence)
#        newplayer.queue(silence)
#    playerLock.acquire()
#    players.append(newplayer)
#    playerLock.release()

def playTone():
    newplayer = pyglet.media.Player()
    for aTuple in PTable:
        tone = aTuple[0]
        newplayer.queue(musicDict[tone])
        newplayer.queue(shortsilence)
    playerLock.acquire()
    players.append(newplayer)
    playerLock.release()

def playChar(charName):
    newplayer = pyglet.media.Player()
    for aTuple in PTable:
        charList = aTuple[1]
        nameFound = False
        for aName in charList:
            if aName == charName:
                nameFound = True
                newplayer.queue(musicDict[aName])
        if not nameFound:
            newplayer.queue(longsilence)
        newplayer.queue(shortsilence)

    playerLock.acquire()
    players.append(newplayer)
    playerLock.release()

def exit_callback(dt):
    pyglet.app.exit()

def fillTable():
    for i in range (0, 8):
        PTable.append ((tones[i%4], [chars1[i%4], chars2[i%4]]))

def main(argv):
    fillTable()
    threads = []
    toneThread = Thread(target=playTone)
    threads.append(toneThread)
    for charName in allChars:
        newThr = Thread(target=playChar, args=(charName,))
        threads.append(newThr)
    #for x in range (0, 6):
    #    newThr = Thread(target=playMusic, args=(x,))
    #    threads.append(newThr)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    pgroup = pyglet.media.PlayerGroup(players)
    pgroup.play()
    pyglet.clock.schedule_once(exit_callback, 30)
    pyglet.app.run()


if __name__ == '__main__':
    main(sys.argv)
