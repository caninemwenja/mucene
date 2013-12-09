from django.contrib import admin
from models import *

class ArticleAdmin(admin.ModelAdmin):
    exclude = ("slug", )

admin.site.register(Article, ArticleAdmin)

class VoteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Vote, VoteAdmin)

