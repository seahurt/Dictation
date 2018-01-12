from django.shortcuts import render,redirect,reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Word
from django.contrib.auth.models import User
from django.http import HttpResponse
from random import randint
#from multiprocessing import Pool,Process
import json
from django.core import serializers


# data = serializers.serialize("xml", SomeModel.objects.all())
# Create your views here.



# @login_required(login_url='/user/login/')
def index(request):
    if request.method=='GET':
        wordlist = Word.objects.all().order_by('?')[:10]
        # wordlist = all[:10]
        context = {
            'wordlist':wordlist
        }
        print(context)
        for word in wordlist:
            if word.pronunciation == '':
                word.Pronunce()
        # time.sleep(2)
        return render(request,'main/index.html',context)


# @login_required(login_url='/user/login/')
def randword(request):
    wordlist = Word.objects.filter(known=False)
    key = randint(0,len(wordlist)-1)
    word = wordlist[key]
    errorlist = Word.objects.filter(error=True)
    knownlist = Word.objects.filter(known=True)
    if (len(errorlist)+len(knownlist))==0:
        correctrate = '0%'
    else:
        correctrate = '%.2f%' %(len(errorlist)/(len(errorlist)+len(knownlist)))
    if word.pronunciation == '':
        word.Pronunce()
    context = {
        # 'word':serializers.serialize('json',[word],ensure_ascii=False),
        # 'errorlist':serializers.serialize('json',list(errorlist),ensure_ascii=False),
        # 'knownlist':serializers.serialize('json',list(knownlist),ensure_ascii=False),
        'word':word,
        'errorlist':errorlist,
        'knownlist':knownlist,
        'errornum':len(errorlist),
        'knownnum':len(knownlist),
        'correctrate':correctrate,
    }
    return render(request,'main/random.html',context)

def randerror(request):
    wordlist = Word.objects.filter(error=True)
    key = randint(0,len(wordlist)-1)
    word = wordlist[key]
    if word.pronunciation == '':
        p = Process(target=word.Pronunce)
        p.start()
        p.join()
    context = {
        'word':word,
    }
    return

def addToErrorList(request):
    """TODO:add login control"""
    english = request.POST['word']
    word = Word.objects.get(spell=english)
    word.error = True
    word.known = False
    word.save()
    return HttpResponse(json.dumps({'success':True}))

def addToKnownList(request):
    english = request.POST['word']
    word = Word.objects.get(spell=english)
    word.known = True
    word.error = False
    word.save()
    return HttpResponse(json({'success':True}))
# @login_required(login_url='/user/login/')
# def addToList(request):
#     pass
#

# def login_view(request):
#     username = request.POST['username']
#     passwd = request.POST['password']
#     DictUser = authenticate(request,username=username,password=passwd)
#     if DictUser is not None:
#         login(request,DictUser)
#         return redirect(reverse('index'))
#     else:
#         return HttpResponse('Error login message!')


# def logout_view(request):
#     logout(request)
#     return redirect(reverse('login') )




