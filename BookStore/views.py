from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.decorators import api_view

from BookStore.forms import SignUpForm
from BookStore.models import Book, Category


@api_view(['GET'])
def homepage(request):
    categories = Category.objects.all()
    return render(request, 'user/home.html', {'categories': categories})


@api_view(['POST', 'GET'])
def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Успешная авторизация")
            return redirect('home')
        else:
            messages.error(request, "Неверный адрес электронной почты или пароль")
            return redirect('login')
    else:
        return render(request, 'login.html', {})


@login_required(login_url='/login')
@api_view(['POST'])
def logout_user(request):
    logout(request)
    return redirect('home')


@api_view(['POST'])
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)


@api_view(['GET'])
def all_books(request):
    # books = Book.objects.all()
    return render(request, 'user/catalog.html')


@api_view(['GET'])
def books_by_author(request, author_id):
    pass


@api_view(['GET'])
def books_by_category(request, category_id):
    pass


@api_view(['GET'])
def book_info(request, book_id):
    pass


@api_view(['GET'])
@login_required(login_url='/login')
def profile(request):
    return render(request, 'user/../templates/profile.html')


@api_view(['POST'])
@login_required(login_url='/login')
def add_book(request):
    pass


@api_view(['PUT'])
@login_required(login_url='/login')
def edit_book(request, book_id):
    pass


@api_view(['DELETE'])
@login_required(login_url='/login')
def delete_book(request, book_id):
    pass


@api_view(['GET', 'POST'])
@login_required(login_url='/login')
def view_cart(request):
    pass


@api_view(['POST'])
@login_required(login_url='/login')
def add_to_cart(request, book_id):
    pass


@api_view(['DELETE'])
@login_required(login_url='/login')
def delete_from_cart(request, book_id):
    pass


@api_view(['POST'])
@login_required(login_url='/login')
def make_order(request, cart_id):
    pass



