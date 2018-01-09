from django.db import models
from django.contrib.auth.models import User
from dictation import settings
import os
from gtts import gTTS
from threading import Thread

# Create your models here.
STATIC_DIR = settings.AUDIO_DIRS
# ABS_AUDIO_DIR = os.path.join(BASE_DIR,settings.STATIC_URL)
ABS_AUDIO_DIR = os.path.join(STATIC_DIR,'main/audio/')
# HOST_AUDIO_DIR = os.path.join(settings.STATIC_URL,'audio')

class Word (models.Model):
    spell = models.CharField(max_length=30,unique=True,blank=False)
    definition = models.CharField(max_length=30)
    example = models.CharField(max_length=500,blank=True)
    pronunciation = models.CharField(max_length=1000,blank=True)
    phonetic_symbol = models.CharField(max_length=100,blank=True)
    level = models.CharField(max_length=20,default='IELTS')
    error = models.BooleanField(default=False)
    known = models.BooleanField(default=False)

    def __str__(self):
        return self.spell

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
        tts = gTTS(text=self.spell, lang='en', slow=False)
        pronunciation = os.path.join(ABS_AUDIO_DIR, self.spell + '.mp3')
        t = Thread(target=tts.save,args=(pronunciation,))
        t.daemon = True
        t.start()
        t.join(timeout=3)
        if t.is_alive():
            return
        self.pronunciation = self.spell+'.mp3'
        self.save()

#
# class Level(models.Model):
#     name = models.CharField(max_length=20)
#     words = models.ManyToManyField(Word)
#
#     return self.name
#     def __str__(self):
#         pass


# class DictUser(User):
#     errorlist = models.ManyToManyField(Word,related_name="error_by_user")
#     seenlist = models.ManyToManyField(Word,related_name="seen_by_user")
#     knownlist = models.ManyToManyField(Word,related_name="known_by_user")

#
# class WordRecord(models.Model):
#     user = models.ForeignKey(User)
#     words = models.ForeignKey(Word)
#     add_time = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         abstract = True
#         ordering = ['-add_time']
#
# class ErrorRecord(WordRecord):
#     class Meta:
#         db_table = "error_record_list"
#
#
# class SeenRecord(WordRecord):
#     class Meta:
#         db_table = "seen_record_list"
#
#
# class KnownRecord(WordRecord):
#     class Meta:
#         db_table = "known_record_list"
#
