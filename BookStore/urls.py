from django.urls import path
from . import views
from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage, name='home'),
    path('login/', views.EmailLoginView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('catalog/', views.all_books, name='catalog'),
]
