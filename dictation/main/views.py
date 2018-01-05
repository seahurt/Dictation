from django.shortcuts import render
from .models import Word
from django.http import HttpResponse
from random import randint
from multiprocessing import Pool
# Create your views here.
def index(request):
    if request.method=='GET':
        wordlist = Word.objects.all().order_by('?')[:10]
        # wordlist = all[:10]
        context = {
            'wordlist':wordlist
        }
        print(context)
        p = Pool(10)
        for word in wordlist:
            if word.pronunciation == '':
                p.apply_async(word.Pronunce)
        p.close()
        p.join()
        # time.sleep(2)
        return render(request,'main/index.html',context)

def randword(request):
    wordlist = Word.objects.all()
    key = randint(0,len(wordlist)-1)
    word = wordlist[key]
    p = Pool()
    if word.pronunciation == '':
        p.apply_async(word.Pronunce)
    p.close()
    p.join()
    context = {'word':word}
    return render(request,'main/random.html',context)