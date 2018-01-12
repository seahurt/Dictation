#!python3
# coding=utf-8
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'dictation.settings'
django.setup()
from main.models import Word
itles = "itles.tsv"
queryset = []
with open(itles) as f:
    content = f.readlines()
    for line in content:
        # print(line)
        word,sync,chinese = line.strip().split('\t')
        explain = '\n'.join([sync,chinese])
        try:
            exist = Word.objects.get(spell=word)
        except BaseException:
            newword = Word(spell=word,definition=explain)
            #newword.save()
            queryset.append(newword)
            print('%s saved' %word)
Word.objects.bulk_create(queryset)
