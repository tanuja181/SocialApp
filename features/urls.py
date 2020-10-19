from django.urls import path


from . import views

app_name = 'features'

urlpatterns = [
    path('', views.home, name='home'),
    path('add_post', views.add_post, name='home'),
    path('search', views.search_users, name='home'),
    path('profile', views.home, name='home'),


]