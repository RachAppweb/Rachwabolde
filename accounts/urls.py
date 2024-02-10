from django.urls import path
from . import views
from . import context_processor

urlpatterns = [
    path('registration/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
    path('resetpassworddasboard/', views.resetpassworddasboard,
         name='resetpassworddasboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('comments/', views.comments, name='comments'),
    # path('comments/', views.displaying, name='comments'),
    path('resetnewpassword/', views.resetnewpassword, name='resetnewpassword'),
    path('rest_activate/<uidb64>/<token>',
         views.reset_password_activation, name='rest_activate'),

    path('activate/<uidb64>/<token>', views.activate, name='activate'),
#     path('error/', views.servererror, name='error'),





]
