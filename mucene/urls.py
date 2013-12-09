from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from articles.views import ArticleListView, ArticleAddView
from articles.views import ArticleDetailView
from articles.views import ArticleEditView, ArticleDeleteView
from profiles.views import UserProfileView, UserProfileEditView

from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', ArticleListView.as_view(), name="home"),
    url(r'^articles/add/$', login_required(ArticleAddView.as_view()), name='article_add'),
    url(r'^articles/(?P<slug>.+)/edit/$', login_required(ArticleEditView.as_view()), name='article_edit'),
    url(r'^articles/(?P<slug>.+)/delete/$', login_required(ArticleDeleteView.as_view()), name='article_delete'),
    url(r'^articles/(?P<slug>.+)/$', ArticleDetailView.as_view(), name='article_detail'),

    url(r'^login/$', "django.contrib.auth.views.login", { "template_name": "login.html" },
        name="login"),
    url(r'^logout/$', "django.contrib.auth.views.logout_then_login", name="logout"),
    url(r'^accounts/', include("registration.backends.simple.urls")),

    url(r'^users/(?P<slug>\w+)/$', UserProfileView.as_view(), name="profile"),
    url(r'^edit_profile/$', login_required(UserProfileEditView.as_view()), name="edit_profile"),
)
