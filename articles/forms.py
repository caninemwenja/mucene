from django import forms
from models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ("author", "written_on", "edited_on", "slug",)

