from django_archive.BookStore.models import Book


def books_sorted_by_cost(order):
    if order == "0":
        return Book.objects.all()
    elif order == "1":
        return Book.objects.order_by('price')
    elif order == "-1":
        return Book.objects.order_by('-price')


def books_sorted_by_alphabet(order):
    if order == "0":
        return Book.objects.all()
    elif order == "1":
        return Book.objects.order_by('title')
    elif order == "-1":
        return Book.objects.order_by('-title')
