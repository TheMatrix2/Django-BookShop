from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Book, Category


class SignUpForm(UserCreationForm):
    middle_name = forms.CharField(
        label="",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            'type': 'middle_name', 'id': 'floatingInput', 'class': 'form-control', 'placeholder': 'Фамилия'}))
    first_name = forms.CharField(
        label="",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            'type': 'first_name', 'id': 'floatingInput', 'class': 'form-control', 'placeholder': 'Имя'}))
    username = forms.EmailField(
        label="",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Электронная почта'}))
    password1 = forms.CharField(
        label="",
        required=True,
        min_length=8,
        max_length=50,
        widget=forms.PasswordInput(attrs={'type': 'password', 'id': 'floatingInput', 'class': 'form-control',
                                          'placeholder': 'Пароль'}), help_text=(
            '<ul class="form-text text-muted small"><li>Пароль не должен быть схожим с'
            ' персональными данными.</li><li>Пароль должен содержать как минимум '
            '8 символов.</li><li>Пароль не должен быть слишком простым.'
            '</li><li>Пароль не должен состоять только из цифр.</li></ul>'))
    password2 = forms.CharField(
        label="",
        required=True, max_length=100, widget=forms.PasswordInput(attrs={
            'type': 'password', 'id': 'floatingInput', 'class': 'form-control', 'placeholder': 'Подтверждение пароля'}), help_text=(
            '<span class="form-text text-muted"><small>Введите пароль еще раз для верификации.</small></span>'))

    class Meta:
        model = User
        fields = ('middle_name', 'first_name', 'username', 'password1', 'password2')

    def __int__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)


class AddBookForm(forms.ModelForm):
    category_choices = Category.objects.values_list('id', 'name')

    title = forms.CharField(
        template_name='Название',
        label="",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            'name': 'title', 'class': 'form-control', 'placeholder': 'Название'}))
    author = forms.CharField(
        template_name='Автор',
        label="",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            'name': 'author', 'type': 'text', 'class': 'form-control', 'placeholder': 'Автор'}), help_text=(
            '<ul class="form-text text-muted small"><li>ФИО автора. Например: Толстой Лев Николаевич.</li></ul>'))
    category = forms.ChoiceField(
        template_name='Категория',
        label="",
        required=True,
        widget=forms.Select(attrs={
            'name': 'category', 'class': 'form-control', 'placeholder': 'Категория'}),
        choices=category_choices)
    description = forms.CharField(
        template_name='Описание',
        label="",
        required=True,
        widget=forms.Textarea(attrs={
            'name': 'description', 'style': 'padding-bottom: 100px', 'class': 'form-control', 'placeholder': 'Описание'}))
    price = forms.FloatField(
        template_name='Цена',
        label="",
        required=True,
        widget=forms.NumberInput(attrs={
            'name': 'price', 'class': 'form-control', 'placeholder': 'Цена'}))
    number_of_pages = forms.IntegerField(
        template_name='Количество страниц',
        label="",
        required=True,
        widget=forms.NumberInput(attrs={
            'name': 'number_of_pages', 'class': 'form-control', 'placeholder': 'Количество страниц'}))
    quantity_in_stock = forms.IntegerField(
        template_name='Количество книг на складе',
        label="",
        required=True,
        widget=forms.NumberInput(attrs={
            'name': 'quantity_in_stock', 'class': 'form-control', 'placeholder': 'Количество на складе'}))

    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'description', 'price', 'number_of_pages', 'quantity_in_stock']


class EditBookForm(forms.ModelForm):
    description = forms.CharField(
        template_name='Описание',
        label="",
        required=True,
        widget=forms.Textarea(attrs={
            'name': 'description', 'style': 'padding-bottom: 100px', 'class': 'form-control',
            'placeholder': 'Описание'}))
    price = forms.FloatField(
        template_name='Цена',
        label="",
        required=True,
        widget=forms.NumberInput(attrs={
            'name': 'price', 'class': 'form-control', 'placeholder': 'Цена'}))
    quantity_in_stock = forms.IntegerField(
        template_name='Количество книг на складе',
        label="",
        required=True,
        widget=forms.NumberInput(attrs={
            'name': 'quantity_in_stock', 'class': 'form-control', 'placeholder': 'Количество на складе'}))

    class Meta:
        model = Book
        fields = ['description', 'price', 'quantity_in_stock']