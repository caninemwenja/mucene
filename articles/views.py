from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from models import *
from forms import ArticleForm
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseForbidden

class AuthorRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        result = super(AuthorRequiredMixin, self).dispatch(request, *args, **kwargs)
        if self.object.author != self.request.user:
            return HttpResponseForbidden("Sorry, you can't modify that article")
        return result

class ArticleListView(ListView):
    model = Article
    queryset = Article.with_votes.all()

class ArticleDetailView(DetailView):
    queryset = Article.with_votes.all()
    slug_field = "slug"

class ArticleAddView(CreateView):
    model = Article
    form_class = ArticleForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(ArticleAddView, self).form_valid(form)

class ArticleEditView(AuthorRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    slug_field = "slug"

    def get_query_set(self):
        return Article.with_votes.filter(author=self.request.user)

class ArticleDeleteView(AuthorRequiredMixin, DeleteView):
    model = Article
    slug_field = "slug"
    success_url = reverse_lazy("home")
    
    def get_query_set(self):
        return Article.with_votes.filter(author=self.request.user)
