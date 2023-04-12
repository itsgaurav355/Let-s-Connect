from django.urls import path 
from . import views
urlpatterns = [
    path('home',views.index , name = 'index'),
    path('',views.home , name = 'main'),
    path('signup',views.signup ,name='signup'),
    path('signin',views.signin, name='signin'),
    path('follow',views.follow, name='follow'),
    path('search',views.search, name='search'),
    path('messages_page',views.messages_page, name='messages_page'),
    path('logout',views.logout, name='logout'),
    path('settings',views.settings,name='settings'),
    path('upload',views.upload,name='upload'),
    path('profile/<str:pk>',views.profile,name='profile'),
    path('like-post',views.like_post,name='like-post'),
    path('review',views.review,name='review')
]