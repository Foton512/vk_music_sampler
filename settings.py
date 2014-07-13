# -*- coding: utf-8 -*-

windowLeft = 100
windowTop = 100
windowWidth = 800
windowHeight = 700

appId = 4434173
authorizedUrl = "https://oauth.vk.com/blank.html"
permissions = 8
authUrl = "https://oauth.vk.com/authorize?client_id={appId}&scope={permissions}&redirect_uri={redirectUrl}&display=page&v=5.21&response_type=token".format(
          appId = appId, permissions = permissions, redirectUrl = authorizedUrl)
audioCount = 6000
maxUserId = 100000000
getAudioUrl = "https://api.vk.com/method/audio.get?owner_id={{userId}}&count={audioCount}".format(
              audioCount = audioCount)
sleepTime = 0.3
sleepTimeIfError = 5
