from django.contrib import admin

from .models import Question, Choice, Valuta, Valuta_kurs

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Valuta)
admin.site.register(Valuta_kurs)
