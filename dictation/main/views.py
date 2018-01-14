from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Word
from django.contrib.auth.models import User
from django.http import HttpResponse
from random import randint
from multiprocessing import Pool, Process
import json
from django.core import serializers
# data = serializers.serialize("xml", SomeModel.objects.all())
# Create your views here.
# @login_required(login_url='/user/login/')


def checkmp3(word):
    if word.pronunciation == '':
        p = Process(target=word.Pronunce)
        p.start()
        p.join()


def index(request):
    if request.method == 'GET':
        wordlist = Word.objects.all().order_by('?')[:10]
        # wordlist = all[:10]
        context = {
            'wordlist': wordlist
        }
        print(context)
        p = Pool(10)
        for word in wordlist:
            if word.pronunciation == '':
                p.apply_async(word.Pronunce)
        p.close()
        p.join()
        # time.sleep(2)
        return render(request, 'main/index.html', context=context)


def wordtest(request, pk):
    word = Word.objects.get(pk=pk)
    next = str(int(pk)+1)
    checkmp3(word)
    context = {
        'word': word,
        'next': next,
    }
    return render(request, 'main/detail.html', context=context)


def stat():
    errorlist = Word.objects.filter(error=True)
    knownlist = Word.objects.filter(known=True)
    errornum = len(errorlist)
    knownnum = len(knownlist)
    if (len(errorlist)+len(knownlist)) == 0:
        correctrate = '0%'
    else:
        correctrate = str(
            len(errorlist)/(len(errorlist)+len(knownlist))*100)+'%'
    return(errorlist, knownlist, errornum, knownnum, correctrate)

# @login_required(login_url='/user/login/')


def randword(request):
    wordlist = Word.objects.filter(known=False)
    key = randint(0, len(wordlist)-1)
    word = wordlist[key]
    checkmp3(word)
    errorlist, knownlist, errornum, knownnum, correctrate = stat()
    context = {
        # 'word':serializers.serialize('json',[word],ensure_ascii=False),
        # 'errorlist':serializers.serialize('json',list(errorlist),ensure_ascii=False),
        # 'knownlist':serializers.serialize('json',list(knownlist),ensure_ascii=False),
        'word': word,
        # 'errorlist': errorlist,
        # 'knownlist': knownlist,
        # 'errornum': errornum,
        # 'knownnum': knownnum,
        # 'correctrate': correctrate,
    }
    return render(request, 'main/random.html', context=context)


def randerror(request):
    wordlist = Word.objects.filter(error=True)
    key = randint(0, len(wordlist)-1)
    word = wordlist[key]
    checkmp3(word)
    context = {
        'word': word,
    }
    return render(request, 'main/randerror.html', context=context)


def statinfo(request):
    errorlist = Word.objects.filter(error=True)
    knownlist = Word.objects.filter(known=True)
    errornum = len(errorlist)
    knownnum = len(knownlist)
    return HttpResponse('statinfo')


def addToErrorList(request):
    """TODO:add login control"""
    english = request.POST['word']
    word = Word.objects.get(spell=english)
    word.error = True
    word.known = False
    word.save()
    return HttpResponse(json.dumps({'success': True}))


def addToKnownList(request):
    english = request.POST['word']
    word = Word.objects.get(spell=english)
    word.known = True
    word.error = False
    word.save()
    return HttpResponse(json({'success': True}))
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
