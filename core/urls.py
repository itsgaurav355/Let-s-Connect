from django.urls import path 
from . import views
urlpatterns = [
    path('home',views.index , name = 'index'),
    path('',views.home , name = 'main'),
    path('signup',views.signup ,name='signup'),
    path('signin',views.signin, name='signin'),
    path('follow',views.follow, name='follow'),
    path('search',views.search, name='search'),
    path('logout',views.logout, name='logout'),
    path('settings',views.settings,name='settings'),
    path('upload',views.upload,name='upload'),
    path('profile/<str:pk>',views.profile,name='profile'),
    path('like-post',views.like_post,name='like-post'),
    path('review',views.review,name='review'),
    path('messages_page', views.messages_page, name='messages_page'),
    path('get_messages/<int:chat_partner_id>', views.get_messages, name='get_messages'),
    path('send_message', views.send_message, name='send_message'),
    path('send_typing', views.send_typing, name='send_typing'),
    path('check_typing/<int:chat_partner_id>', views.check_typing, name='check_typing'),
]