from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/', views.post_item, name='post_item'),
    #path('add/', views.add_lost_item, name='add_item'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="findme/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('logout/', views.logout_view, name='logout'),
    path('chat/start/<int:item_id>/', views.start_chat, name='start_chat'),
    path('chat/<int:room_id>/', views.chat_room, name='chat_room'),
    path("notifications/", views.notifications, name="notifications"),



]
