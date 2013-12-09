from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy

class ArticleVoteCountManager(models.Manager):
    def get_query_set(self):
        return super(ArticleVoteCountManager, self).get_query_set().annotate(
            votes = Count('vote')).order_by("-votes")

class Article(models.Model):
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    author = models.ForeignKey(User)
    written_on = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)
    slug = models.SlugField()

    with_votes = ArticleVoteCountManager()
    objects = models.Manager() # default manager

    #def votes(self):
    #    up = self.vote_set.filter(vote_type__exact=True).count()
    #    down = self.vote_set.filter(vote_type__exact=False).count()
    #    return up - down

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy("article_detail", kwargs = { "slug": self.slug })

class Vote(models.Model):
    vote_type = models.BooleanField() # up or down
    article = models.ForeignKey(Article)
    voter = models.ForeignKey(User)

    def vote_str(self):
        if self.vote_type:
            return "up"
        return "down"

    def __unicode__(self):
        return "%s %s voted %s" % (self.voter.username, self.vote_str(),
            self.article.title)

from django.template.defaultfilters import slugify
def slugify_article_title(sender, instance, raw, **kwargs):
    instance.slug = slugify(instance.title.lower())

from django.db.models.signals import pre_save
pre_save.connect(slugify_article_title, Article)
