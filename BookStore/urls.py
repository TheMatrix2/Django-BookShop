from django.urls import path
from . import views
from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('catalog/', views.catalog, name='catalog'),
    path('book-info/<int:book_id>', views.book_info, name='book_info'),
    path('add-to-cart/<int:book_id>', views.add_to_cart, name='add_to_cart'),
    path('delete-from-cart/<int:book_id>', views.delete_from_cart, name='delete_from_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('order/<int:cart_id>', views.make_order, name='order'),

    path('staff/', views.staff_profile, name='staff_profile'),
    path('staff/add-book/', views.add_book, name='add_book'),
    path('staff/edit-book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('staff/delete-book/<int:book_id>/', views.delete_book, name='delete_book'),
]
