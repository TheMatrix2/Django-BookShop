from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Book, Category


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Электронная почта'}))
    middle_name = forms.CharField(
        label="",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Фамилия'}))
    first_name = forms.CharField(
        label="",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Имя'}))
    password = forms.CharField(
        label="",
        required=True,
        min_length=8,
        max_length=50,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}), help_text=(
            '<ul class="form-text text-muted small"><li>Пароль не должен быть схожим с'
            ' персональными данными.</li><li>Пароль должен содержать как минимум '
            '8 символов.</li><li>Пароль не должен быть слишком простым.'
            '</li><li>Пароль не должен состоять только из цифр.</li></ul>'))
    confirm_password = forms.CharField(
        label="",
        required=True, max_length=100, widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Подтверждение пароля'}), help_text=(
            '<span class="form-text text-muted"><small>Введите пароль еще раз для верификации.</small></span>'))

    class Meta:
        model = User
        fields = ('middle_name', 'first_name', 'last_name', 'email', 'password', 'confirm_password')

    def __int__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)


class AddBookForm(forms.ModelForm):
    category_choices = Category.objects.values_list('id', 'name')

    title = forms.CharField(
        label="",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Название'}))
    author = forms.CharField(
        label="",
        required=True,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Автор'}), help_text=(
            '<ul class="form-text text-muted small"><li>ФИО автора. Например: Толстой Лев Николаевич.</li></ul>'))
    category = forms.ChoiceField(
        label="",
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control', 'placeholder': 'Категория'}),
        choices=category_choices)
    description = forms.CharField(
        label="",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Описание'}))
    price = forms.FloatField(
        label="",
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'placeholder': 'Цена'}))
    number_of_pages = forms.IntegerField(
        label="",
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'placeholder': 'Количество страниц'}))
    quantity = forms.IntegerField(
        label="",
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 'placeholder': 'Количество на складе'}))

    class Meta:
        model = Book
        fields = '__all__'


# class EditBookForm(forms.ModelForm):
