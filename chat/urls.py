from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^add_friend/$', views.AddFriendView.as_view(), name='add_friend'),
]
