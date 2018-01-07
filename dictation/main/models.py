from django.db import models
from dictation import settings
import os
from gtts import gTTS
# Create your models here.
STATIC_DIR = settings.AUDIO_DIRS
# ABS_AUDIO_DIR = os.path.join(BASE_DIR,settings.STATIC_URL)
ABS_AUDIO_DIR = os.path.join(STATIC_DIR,'main/audio/')
# HOST_AUDIO_DIR = os.path.join(settings.STATIC_URL,'audio')

class Word (models.Model):
    english = models.CharField(max_length=30)
    chinese = models.CharField(max_length=30)
    example = models.CharField(max_length=500,blank=True)
    pronunciation = models.CharField(max_length=1000,blank=True)

    def __str__(self):
        return self.english

    def Pronunce(self):
        # # Baidu AIP init
        # APP_ID = '1069905'
        # API_KEY = '8qkYNr9Z5UU42jt3rjQM7qRs'
        # SECRET_KEY = '914n7nalziwKsPHb2w4h7yAcuvIbNY0W'
        # aipSpeech = AipSpeech(APP_ID,API_KEY,SECRET_KEY)
        # result = aipSpeech.synthesis(self.English,'en',1,{
        #     'vol':5,
        #     'spd':4,
        #
        # })
        # if not isinstance(result,dict):
        #     pronunciation = os.path.join(AUDIO_DIR,self.English+'.mp3')
        #     with open(pronunciation,'wb') as p:
        #         p.write(result)
        #         self.Pronunciation = pronunciation
        # else:
        #     print(result)
        #gtts
        tts = gTTS(text=self.english, lang='en')
        pronunciation = os.path.join(ABS_AUDIO_DIR, self.english + '.mp3')
        tts.save(pronunciation)
        self.pronunciation = self.english+'.mp3'
        super(Word,self).save()

