from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from dictation import settings
import os
from gtts import gTTS
from threading import Thread
from google.cloud import storage
import re, requests, warnings
from six.moves import urllib
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from gtts_token.gtts_token import Token
# Create your models here.
#STATIC_DIR = settings.AUDIO_DIRS
## ABS_AUDIO_DIR = os.path.join(BASE_DIR,settings.STATIC_URL)
#ABS_AUDIO_DIR = os.path.join(STATIC_DIR,'main/audio/')
## HOST_AUDIO_DIR = os.path.join(settings.STATIC_URL,'audio')

class GTTS_TO_GCS(gTTS):
    
    def upload_to_gcs(self,word):
        CLOUD_STORAGE_BUCKET = os.environ['CLOUD_STORAGE_BUCKET']
#        CLOUD_STORAGE_BUCKET = 'dictation-static'
        client = storage.Client()
        bucket = client.get_bucket(CLOUD_STORAGE_BUCKET)
        blob = bucket.blob('static/main/audio/'+word.spell+'.mp3')
        if blob is None:
            print('this blog is none')
#       blob.upload_from_string()
        data = b''
        """ Do the Web request and save to a byte string """
        for idx, part in enumerate(self.text_parts):
            payload = { 'ie' : 'UTF-8',
                        'q' : part,
                        'tl' : self.lang,
                        'ttsspeed' : self.speed,
                        'total' : len(self.text_parts),
                        'idx' : idx,
                        'client' : 'tw-ob',
                        'textlen' : self._len(part),
                        'tk' : self.token.calculate_token(part)}
            headers = {
                "Referer" : "http://translate.google.com/",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"
                }
            if self.debug: print(payload)
            try:
                # Disable requests' ssl verify to accomodate certain proxies and firewalls
                # Filter out urllib3's insecure warnings. We can live without ssl verify here
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=InsecureRequestWarning)
                    r = requests.get(self.GOOGLE_TTS_URL,
                                     params=payload,
                                     headers=headers,
                                     proxies=urllib.request.getproxies(),
                                     verify=False)
                if self.debug:
                    print("Headers: {}".format(r.request.headers))
                    print("Request url: {}".format(r.request.url))
                    print("Response: {}, Redirects: {}".format(r.status_code, r.history))
                r.raise_for_status()
                for chunk in r.iter_content(chunk_size=1024):
                    data += chunk
        
            except Exception as e:
                raise
        blob.upload_from_string(data, content_type='audio/mpeg')
        word.pronunciation = blob.public_url
        word.save()


@python_2_unicode_compatible
class Word (models.Model):
    spell = models.CharField(max_length=50,unique=True,blank=False)
    definition = models.CharField(max_length=300)
    example = models.CharField(max_length=500,blank=True)
    pronunciation = models.CharField(max_length=1000,blank=True)
    phonetic_symbol = models.CharField(max_length=100,blank=True)
    level = models.CharField(max_length=20,default='IELTS')
    error = models.BooleanField(default=False)
    known = models.BooleanField(default=False)

    def __str__(self):
        return self.spell

    def Pronunce(self):
        tts = GTTS_TO_GCS(text=self.spell, lang='en', slow=False)
#        pronunciation = os.path.join(ABS_AUDIO_DIR, 'audio.mp3')
        t = Thread(target=tts.upload_to_gcs,args=(self,))
        t.daemon = True
        t.start()
        t.join(timeout=3)
        if t.is_alive():
            return
