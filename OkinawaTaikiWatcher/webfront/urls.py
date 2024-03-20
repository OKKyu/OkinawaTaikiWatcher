from django.urls import path, include
from . import views

# appが複数ある場合には、app_nameをもとにアプリを識別する。
# app_name = 'webfront'
urlpatterns = [
    path('login', views.login_app, name='login'),
    path('authentication', views.authentication, name='authentication'),
    path('topview', views.topview, name='topview'),
    path('logout', views.logout_app, name='logout'),
    path('update_infos', views.update_infos, name='update_infos'),
]
