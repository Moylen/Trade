from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from .models import Product, Category, ProductImage, Comment, UserAccount


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('user', 'removed')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'title': 'Название',
            'price': 'Цена',
            'description': 'Описание',
            'address': 'Адрес',
            'category': 'Категория'
        }


class ProductImageForm(forms.Form):
    img1 = forms.ImageField(label='Изображение', required=True,
                            widget=forms.FileInput(attrs={'class': 'form-control'}))
    img2 = forms.ImageField(label='Изображение', required=False,
                            widget=forms.FileInput(attrs={'class': 'form-control'}))
    img3 = forms.ImageField(label='Изображение', required=False,
                            widget=forms.FileInput(attrs={'class': 'form-control'}))
    img4 = forms.ImageField(label='Изображение', required=False,
                            widget=forms.FileInput(attrs={'class': 'form-control'}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('product', 'user')
        labels = {
            'comment': 'Комментарий',
        }
        widgets = {
            'comment': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Напишите комментарий', 'cols': 20, 'rows': 5})
        }


class RegisterUserForm(forms.ModelForm):
    password_repeat = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повтор пароля'})
    )
    phone = forms.CharField(
        min_length=12,
        max_length=12,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}),
        validators=[
            RegexValidator(regex='^\\+?\\d{11}$', message='Введите корректный номер телефона. Пример: +71234567890'),
        ]
    )

    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {
            'username': 'Почта',
            'password': 'Пароль'
        }
        widgets = {
            'username': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Почта'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
        }
        help_texts = {
            'username': None,
            'password': None
        }


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'})
        }


class EditUserAccountForm(forms.ModelForm):
    phone = forms.CharField(
        min_length=12,
        max_length=12,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон'}),
        validators=[
            RegexValidator(regex='^\\+?\\d{11}$', message='Введите корректный номер телефона. Пример: +71234567890'),
        ]
    )

    class Meta:
        model = UserAccount
        fields = ('phone',)


class LoginUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {
            'username': 'Почта',
            'password': 'Пароль'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Почта'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
        }
        help_texts = {
            'username': None,
            'password': None
        }


class ChangePassUserForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Старый пароль'}), required=True)
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Новый пароль'}), required=True)
    repeat_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повтор нового пароля'}),
        required=True)


class SearchForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control me-2', 'placeholder': 'Поиск'}),
        required=False
    )
