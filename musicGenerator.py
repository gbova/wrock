#musicGenerator.py
#! /usr/bin/env python

import sys
import threading
from threading import Thread
import pyglet
from pyglet import media

longsilence = pyglet.media.load('hp_music/silence_10.wav', streaming=False)

class musicGenerator:
    def __init__(self, data, maxTime, charFile, toneFile):
        self.PTable = data
        self.numChars = numChars
        self.charDict = self.unpackFile (charFile)
        self.toneDict = self.unpackFile (toneFile)
        self.players = []
        self.playerLock = Threading.Lock()
        self.maxTime = maxTime

    def unpackFile (fname):
        newDict = {}
        with open(fname,'r') as f:
            for line in f:
                words = line.split()
                newDict[words[0]] = pyglet.media.load(words[1], streaming=False)
        return newDict

    def start(self):
        threads = []
        toneThread = Thread(target=self.playTone)
        threads.append(toneThread)
        for charName in self.charDict:
            newThread = Thread(target=playChar, args=(charName,))
            threads.append(newThread)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        pgroup = pyglet.media.PlayerGroup(self.players)
        pgroup.play()
        pyglet.clock.schedule_once(self.exit_callback, self.maxTime)
        pyglet.app.run()

    def exit_callback(dt):
        pyglet.app.exit()

    def playTone(self):
        newplayer = pyglet.media.Player()
        for par in self.PTable:
            tone = par[0]
            newplayer.queue(self.toneDict[tone])
            #newplayer.queue(shortsilence)
        self.playerLock.acquire()
        self.players.append(newplayer)
        self.playerLock.release()

    def playChar(self, charName):
        newplayer = pyglet.media.Player()
        for par in self.PTable:
            charList = par[1]
            nameFound = False
            for aName in charList:
                if aName == charName:
                    nameFound = True
                    newplayer.queue(self.charDict[aName])
            if not nameFound:
                newplayer.queue(longsilence)
            #newplayer.queue(shortsilence)
        self.playerLock.acquire()
        self.players.append(newplayer)
        self.playerLock.release()
