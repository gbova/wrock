#music1.py
#test of multithreaded music queueing
# 1 tone thread and 8 character threads go through and example
# table and add their music to the queue

#! /usr/bin/env python

import sys
import threading
from threading import Thread
import pyglet
from pyglet import media

player = pyglet.media.Player()
playerLock = threading.Lock()

IOLock = threading.Lock()
numPlaying = 0
totalThreads = 9
counterMutex = threading.Lock()
allArrived = threading.Lock()
allDone = threading.Lock()

PTable = []

chars1 = ["Harry", "Ron", "Hermione", "Malfoy"]
chars2 = ["Voldemort", "Hagrid", "Dumbledoor", "Dursley"]
allChars = chars1 + chars2
tones = ["joy", "exciting", "tentative", "neutral"]

#music files
hp1 = pyglet.media.load('hp_music/harry_potter.wav', streaming=False)
hp2 = pyglet.media.load('hp_music/harry_potter-2.wav', streaming=False)
hogwarts = pyglet.media.load('hp_music/happy_hogwarts.wav', streaming=False)
christmas = pyglet.media.load('hp_music/hogwarts_christmas.wav', streaming=False)
laugh = pyglet.media.load('hp_music/voldemort_laugh.wav', streaming=False)

musicDict = {"joy": christmas, "neutral" : hogwarts, "tentative" : hp1,
             "exciting" : hp2, "Voldemort" : laugh}

def playTone():
    global numPlaying
    for aTuple in PTable:
        tone = aTuple[0]
        counterMutex.acquire()
        numPlaying += 1
        if numPlaying == totalThreads:
            allDone.acquire()
            allArrived.release()
        counterMutex.release()
        allArrived.acquire()
        allArrived.release()

        playerLock.acquire()
        player.queue(musicDict[tone])
        playerLock.release()

        counterMutex.acquire()
        numPlaying -= 1
        if numPlaying == 0:
            allArrived.acquire()
            allDone.release()
        counterMutex.release()
        allDone.acquire()
        allDone.release()

def playChar(charName):
    global numPlaying
    for aTuple in PTable:
        charList = aTuple[1]
        counterMutex.acquire()
        numPlaying += 1
        if numPlaying == totalThreads:
            allDone.acquire()
            allArrived.release()
        counterMutex.release()
        allArrived.acquire()
        allArrived.release()

        for aName in charList:
            if aName == charName:
                if aName == "Voldemort":
                    playerLock.acquire()
                    player.queue(musicDict[aName])
                    playerLock.release()

        counterMutex.acquire()
        numPlaying -= 1
        if numPlaying == 0:
            allArrived.acquire()
            allDone.release()
        counterMutex.release()
        allDone.acquire()
        allDone.release()

def fillTable():
    for i in range (0, 8):
        PTable.append ((tones[i%4], [chars1[i%4], chars2[i%4]]))

def main(argv):
    fillTable()
    print(PTable)

    allArrived.acquire()
    threads = []
    toneThread = Thread(target=playTone)
    threads.append(toneThread)
    for charName in allChars:
        newThr = Thread(target=playChar, args=(charName,))
        threads.append(newThr)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    player.play()
    pyglet.app.run()


if __name__ == '__main__':
    main(sys.argv)
