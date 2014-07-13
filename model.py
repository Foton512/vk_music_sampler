# -*- coding: utf-8 -*-

from PyQt4.QtCore import QObject, pyqtSignal
from threading import Thread
from settings import *
from random import randint, shuffle
from time import sleep

class Model(QObject):
    infoReady = pyqtSignal(str)

    def __init__(self, vkRequestProcessor):
        QObject.__init__(self)
        self.vkRequestProcessor = vkRequestProcessor

    def getVkRequestProcessor(self):
        return self.vkRequestProcessor

    def setAccessToken(self, accessToken):
        self.accessToken = accessToken

    def setNUsers(self, nUsers):
        self.nUsers = nUsers

    def setSampleSize(self, sampleSize):
        self.sampleSize = sampleSize

    def prepareSampleAsync(self):
        thread = Thread(target = self.prepareSample)
        thread.setDaemon(True)
        thread.start()

    def prepareSample(self):
        i = 0
        usedUserIds = set()
        audios = set()
        while i < self.nUsers:
            while True:
                userId = randint(1, maxUserId)
                if userId not in usedUserIds:
                    usedUserIds.add(userId)
                    break

            response = self.vkRequestProcessor.sendRequest(getAudioUrl.format(userId = userId))
            if response == None or type(response) != list:
                continue
            nResponses = response[0]
            if nResponses == 0:
                continue
            
            for audio in response[1:]:
                audios.add((audio["artist"], audio["title"], audio["genre"] if "genre" in audio else 0))
            i += 1
            self.infoReady.emit("Users processed: {nUsersCurrent}/{nUsers}".format(
                                nUsersCurrent = i, nUsers = self.nUsers))

            #sleep(0.3)

        audiosList = list(audios)
        shuffle(audiosList)
        audiosList = audiosList[:self.sampleSize]

        self.infoReady.emit("Writing sample file...")
        sampleFile = open("sample.txt", "w")
        for audio in audiosList:
            sampleFile.write("{artist}\t{title}\t{genre}\n".format(
                             artist = audio[0].encode("utf-8"),
                             title = audio[1].encode("utf-8"),
                             genre = audio[2]))
        sampleFile.close()
        self.infoReady.emit("Writing sample file completed")
