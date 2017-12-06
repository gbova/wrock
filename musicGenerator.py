# musicGenerator.py
# Contains class definition of musicGenerator
#! /usr/bin/env python

import sys
import threading
from threading import Thread
import pyglet
from pyglet import media

longsilence = pyglet.media.load('hp_music/silence_10.wav', streaming=False)
shortsilence = pyglet.media.load('hp_music/silence_1.wav', streaming=False)


class musicGenerator:
    def __init__(self, data, maxTime, charFile, toneFile):
        """Initialize an instance of the musicGenerator class, given a
        dictionary of tone/character data for each paragraph, a max amount of
        time, and 2 files containing lists of chars/tones and their music"""
        self.PTable = data
        self.tableLen = len(self.PTable)
        self.charDict = self.unpackFile(charFile)
        self.toneDict = self.unpackFile(toneFile)
        self.players = []
        self.playerLock = threading.Lock()
        self.maxTime = maxTime

    def unpackFile (self, fname):
        """Given the name of a file, unpack the characters or tones inside the
        file and their corresponding music pieces into a dictionary to be
        returned"""
        newDict = {}
        with open(fname,'r') as f:
            for line in f:
                words = line.partition(": ")
                music = words[2].strip('\n')
                newDict[words[0]] = pyglet.media.load(str(music), streaming=False)
        return newDict

    def start(self):
        """Start tone and character threads to read music data and queue music
        to play in an order, then play all resulting queues simultaneously"""
        threads = []
        # set up tone thread
        toneThread = Thread(target=self.playTone)
        threads.append(toneThread)
        # set up character threads
        for charName in self.charDict:
            newThread = Thread(target=self.playChar, args=(charName,))
            threads.append(newThread)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # play all players at the same time
        pgroup = pyglet.media.PlayerGroup(self.players)
        pgroup.play()
        # halt music playing after maxTime is reached
        pyglet.clock.schedule_once(self.exit_callback, self.maxTime)
        pyglet.app.run()

    def exit_callback(self, dt):
        """ Exit the pyglet app """
        pyglet.app.exit()

    def playTone(self):
        """ For each paragraph in the table, queue appropriate music for the
        tone to a pyglet player"""
        newplayer = pyglet.media.Player()
        # loop through every paragraph in the table, in order
        for p in range (1, self.tableLen + 1):
            pInfo = self.PTable[p]
            tone = pInfo["tone"]
            newplayer.queue(self.toneDict[tone])
            # small break before next paragraph
            newplayer.queue(shortsilence)
        # add player to shared player list
        self.playerLock.acquire()
        self.players.append(newplayer)
        self.playerLock.release()

    def playChar(self, charName):
        """For each paragraph in the table, queue the music for the given
        character to a pyglet player if they appear"""
        newplayer = pyglet.media.Player()
        # loop through every paragraph in table
        for p in range (1, self.tableLen + 1):
            pInfo = self.PTable[p]
            charList = pInfo["characters"]
            nameFound = False
            # search for character in charList for paragraph
            for aName in charList:
                if aName == charName:
                    nameFound = True
                    newplayer.queue(self.charDict[aName])
                    break;
            # queue silence if not found
            if not nameFound:
                newplayer.queue(longsilence)
            # small break before next paragraph
            newplayer.queue(shortsilence)
        # add player to shared player list
        self.playerLock.acquire()
        self.players.append(newplayer)
        self.playerLock.release()
