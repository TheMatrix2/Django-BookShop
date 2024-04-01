from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.decorators import api_view

from BookStore.forms import SignUpForm, AddBookForm, EditBookForm
from BookStore.models import Book, Category, Author, Cart, CartItem, Order, OrderItem
from .books import books_sorted_by_alphabet, books_sorted_by_cost


# декоратор для ограничения доступа к разделам staff
def staff_required(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return func(request, *args, **kwargs)
        else:
            messages.error(request, 'У вас недостаточно прав, чтобы перейти в этот раздел')
            return redirect('home')
    return wrapper


def superuser_error(func):
    def wrapper(request, *args, **kwargs):
        previous_url = request.META.get('HTTP_REFERER', '/')
        if not request.user.is_superuser:
            return func(request, *args, **kwargs)
        else:
            messages.error(request, 'С правами суперпользователя нельзя взаимодействовать с корзиной и заказом.'
                                    ' Авторизируйтесь как обычный пользователь или зарегистрируйте нового.')
            return redirect(previous_url)
    return wrapper


@api_view(['GET'])
def homepage(request):
    categories = Category.objects.all()
    return render(request, 'user/home.html', {'categories': categories})


@api_view(['POST', 'GET'])
def login_user(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
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
@api_view(['POST', 'GET'])
def logout_user(request):
    logout(request)
    return redirect('home')


@api_view(['POST', 'GET'])
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            Cart.objects.create(user_id=request.user.id, total_price=0)
            messages.success(request, "Успешная регистрация")
            return redirect('home')
    form = SignUpForm()
    return render(request, 'register.html', {'form': form})


@api_view(['GET'])
def catalog(request):
    categories = Category.objects.all()
    authors = Author.objects.all()
    books = Book.objects.all()
    cart_items = CartItem.objects.all()
    if request.method == 'GET':
        alphabet_sort = request.GET.get('alphabetSort')
        cost_sort = request.GET.get('costSort')
        category_filter = request.GET.get('categoryFilter')
        author_filter = request.GET.get('authorFilter')
        if alphabet_sort and alphabet_sort != "0":
            books = books_sorted_by_alphabet(alphabet_sort)
        elif cost_sort and cost_sort != "0":
            books = books_sorted_by_cost(cost_sort)
        elif category_filter and category_filter != "0":
            books = Book.objects.filter(category_id=category_filter)
        elif author_filter and author_filter != "0":
            books = Book.objects.filter(author_id=author_filter)
    return render(request, 'user/catalog.html', {
        'books': books,
        'authors': authors,
        'categories': categories,
        'cart': cart_items})


@api_view(['GET'])
def book_info(request, book_id):
    book = Book.objects.get(id=book_id)
    if book:
        return render(request, 'user/book_info.html', {'book': book})


@api_view(['GET'])
@login_required(login_url='/login')
@superuser_error
def view_cart(request):
    previous_url = request.META.get('HTTP_REFERER', '/')
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    books_in_cart = [Book.objects.get(id=item.book_id) for item in items]
    return render(request, 'user/cart.html', {'books': books_in_cart, 'cart': cart})


@api_view(['POST', 'GET'])
@login_required(login_url='/login')
@superuser_error
def add_to_cart(request, book_id):
    previous_url = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        if request.user.is_superuser:
            messages.error(request, '')
        cart = Cart.objects.get(user_id=request.user.id)
        book = Book.objects.get(id=book_id)
        if CartItem.objects.filter(book_id=book.id, cart_id=cart.id):
            messages.error(request, 'Книга уже в корзине')
        else:
            CartItem.objects.create(cart=cart, book=book, quantity=1)
            cart.total_price += book.price
            cart.save()
            messages.success(request, 'Книга добавлена в корзину')
    return redirect(previous_url)


@api_view(['GET', 'POST', 'DELETE'])
@login_required(login_url='/login')
@superuser_error
def delete_from_cart(request, book_id):
    previous_url = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        book = Book.objects.get(id=book_id)
        cart = Cart.objects.get(user_id=request.user.id)
        to_delete = CartItem.objects.get(book_id=book.id, cart_id=cart.id)
        if to_delete:
            cart.total_price -= to_delete.book.price
            cart.save()
            to_delete.delete()
            messages.success(request, 'Книга удалена из корзины')
    return redirect(previous_url)


@api_view(['GET', 'POST'])
@login_required(login_url='/login')
@superuser_error
def make_order(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    if request.method == 'POST':
        items = CartItem.objects.filter(cart=cart, cart__user_id=request.user.id)
        order = Order.objects.create(user=request.user, total_price=cart.total_price)
        for item in items:
            OrderItem.objects.create(order_id=order.id, book=item.book, quantity=item.quantity, price=item.book.price)
            item.delete()
        messages.success(request, 'Заказ создан')
    return render(request, 'user/home.html')


@api_view(['GET'])
@login_required(login_url='/login')
@staff_required
def staff_profile(request):
    books = Book.objects.all()
    return render(request, 'staff/profile.html', {'books': books})


@api_view(['GET', 'POST'])
@login_required(login_url='/login')
@staff_required
def add_book(request):
    form = AddBookForm(request.POST or None)
    previous_url = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        author = Author.objects.get_or_create(name=request.POST['author'])
        Book.objects.create(
            title=request.POST['title'],
            author=author[0],
            category=Category.objects.get(pk=request.POST['category']),
            description=request.POST['description'],
            price=request.POST['price'],
            number_of_pages=request.POST['number_of_pages'],
            quantity_in_stock=request.POST['quantity_in_stock'])
        messages.success(request, 'Книга добавлена')
        return redirect('staff_profile')
    else:
        return render(request, 'staff/add_book.html', {'form': form,
                                                       'previous_url': previous_url})


@api_view(['GET', 'POST'])
@login_required(login_url='/login')
@staff_required
def edit_book(request, book_id):
    previous_url = request.META.get('HTTP_REFERER', '/')
    to_edit = Book.objects.get(id=book_id)
    form = EditBookForm(request.POST or None, instance=to_edit)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Информация о книге обновлена')
    return render(request, 'staff/edit_book.html', {
        'form': form,
        'book': to_edit,
        'previous_url': previous_url})


@api_view(['GET', 'DELETE', 'POST'])
@login_required(login_url='/login')
@staff_required
def delete_book(request, book_id):
    to_delete = Book.objects.get(id=book_id)
    if request.method == 'POST':
        to_delete.delete()
        messages.success(request, 'Информация о книге удалена')
        return redirect('staff_profile')
    else:
        return render(request, 'staff/edit_book.html', {'book': to_delete})
