from django.conf.urls import url
from . import views



urlpatterns = [
    #blog/
    url(r'^$', views.index, name='index' ),
    #register/
    url(r'^register/$', views.register, name='register'),
    #login/
    url(r'^login/$', views.user_login, name='login'),
    #logout/
    url(r'^logout/$', views.user_logout, name='logout'),
    #blog/archive/
    url(r'^archive/$', views.archive, name='archive'),
    #blog/post_id/
    url(r'^(?P<post_id>\d+)/$', views.detail, name='detail'),
    #blog/addpost/
    url(r'^addpost/$', views.create_post, name='addpost'),
    #blog/post/post_id/delete/
    url(r'^post/(?P<post_id>[0-9]+)/delete/$', views.delete_post, name='deletepost'),

]