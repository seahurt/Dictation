from django.contrib import admin
from .models import Word
# Register your models here.
class WordAdmin(admin.ModelAdmin):
    search_fields = ['english']
admin.site.register(Word,WordAdmin)