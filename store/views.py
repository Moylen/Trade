from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from .forms import RegisterUserForm, LoginUserForm, ProductForm, ProductImageForm, EditUserForm, EditUserAccountForm, \
    ChangePassUserForm, CommentForm, SearchForm
from django.contrib.auth.models import User
from .models import UserAccount, Product, ProductImage, Comment, Favourite
from datetime import datetime, timedelta


class IndexView(View):
    @staticmethod
    def get(request):
        products = Product.objects.filter(removed=False)
        context = {
            'SearchForm': SearchForm(),
            'images': ProductImage.objects.distinct('product').filter(product__in=products)
        }
        return render(request, 'store/index.html', context)

    @staticmethod
    def post(request):
        form = SearchForm(request.POST)
        if form.is_valid():
            products = Product.objects.filter(removed=False, title__contains=form.cleaned_data.get('title'))
            context = {
                'images': ProductImage.objects.distinct('product').filter(product__in=products),
                'SearchForm': SearchForm(request.POST)
            }
            return render(request, 'store/index.html', context)
        else:
            return redirect('index')


class RegisterUserView(View):
    @staticmethod
    def get(request):
        return render(request, 'store/user_register.html', {'form': RegisterUserForm()})

    @staticmethod
    def post(request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['password_repeat']:
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password']
                )
                UserAccount.objects.create(
                    account=user,
                    phone=form.cleaned_data['phone']
                )
                return redirect('user_login')
            return render(request, 'store/user_register.html', {'form': form, 'pass_error': 'Пароли не совпадают'})
        return render(request, 'store/user_register.html', {'form': form})


class LoginUserView(View):
    @staticmethod
    def get(request):
        return render(request, 'store/user_login.html', {'form': LoginUserForm()})

    @staticmethod
    def post(request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = redirect('profile')
            response.set_cookie(
                key='login_date',
                value=f'{datetime.now()}',
                max_age=60 * 60 * 24 * 365,
                expires=f'{datetime.now() + timedelta(days=365)}'
            )
            return response
        else:
            return render(
                request,
                'store/user_login.html',
                {'form': LoginUserForm(request.POST), 'login_error': 'Неверный логин или пароль'}
            )


class LogoutUserView(View):

    @staticmethod
    @login_required(login_url=reverse_lazy('user_login'))
    def get(request):
        logout(request)
        return redirect('user_login')


class CreateProductHandler(View):
    @staticmethod
    @login_required(login_url=reverse_lazy('user_login'))
    def post(request):
        product_form = ProductForm(request.POST)
        image_form = ProductImageForm(request.POST, request.FILES)
        if product_form.is_valid() and image_form.is_valid():
            product = Product.objects.create(**product_form.cleaned_data, user=request.user)
            for img in image_form.cleaned_data.values():
                if img is not None:
                    ProductImage.objects.create(img=img, product=product)
            return redirect('profile')


class AdvertisementGetAJAX(View):
    @staticmethod
    def get(request):
        products = Product.objects.filter(user=request.user, removed=False)
        products_json = serializers.serialize('json', products)
        return HttpResponse(products_json, content_type='application/json')


class AdvertisementDeleteAJAX(View):
    @staticmethod
    def get(request, pk):
        product = Product.objects.get(pk=pk)
        product.removed = True
        product.save()
        return HttpResponse('200')


class ProfileView(View):
    @staticmethod
    @login_required(login_url=reverse_lazy('user_login'))
    def get(request):
        account = UserAccount.objects.get(account=request.user)
        context = {
            'favourites': Favourite.objects.filter(user=request.user),
            'EditUserForm': EditUserForm(instance=request.user),
            'EditUserAccountForm': EditUserAccountForm(instance=account),
            'ProductForm': ProductForm(),
            'ImageForm': ProductImageForm()
        }
        return render(request, 'store/profile.html', context)

    @staticmethod
    @login_required(login_url=reverse_lazy('user_login'))
    def post(request):
        edit_user = EditUserForm(request.POST)
        account_user = EditUserAccountForm(request.POST)
        if edit_user.is_valid() and account_user.is_valid():
            first_name = edit_user.cleaned_data.get('first_name')
            last_name = edit_user.cleaned_data.get('last_name')
            phone = account_user.cleaned_data.get('phone')
            User.objects.filter(username=request.user.username).update(first_name=first_name, last_name=last_name)
            UserAccount.objects.filter(account=request.user).update(phone=phone)
            return redirect('profile')
        else:
            context = {
                'EditUserForm': edit_user,
                'EditUserAccountForm': account_user,
                'ProductForm': ProductForm(),
                'ImageForm': ProductImageForm(),
                'Products': Product.objects.filter(user=request.user)
            }
            return render(request, 'store/profile.html', context)


class ChangePasswordUserView(View):
    @staticmethod
    @login_required(login_url=reverse_lazy('user_login'))
    def get(request):
        return render(request, 'store/user_change_pass.html', {'form': ChangePassUserForm()})

    @staticmethod
    @login_required(login_url=reverse_lazy('user_login'))
    def post(request):
        form = ChangePassUserForm(request.POST)
        user = User.objects.get(username=request.user.username)
        if form.is_valid():
            old_pass = form.cleaned_data.get('old_password')
            new_pass = form.cleaned_data.get('new_password')
            new_pass_repeat = form.cleaned_data.get('repeat_new_password')
            if not check_password(old_pass, user.password):
                return render(
                    request,
                    'store/user_change_pass.html',
                    {'form': form, 'error': 'Старый пароль не совпадает'}
                )
            if new_pass != new_pass_repeat:
                return render(
                    request,
                    'store/user_change_pass.html',
                    {'form': form, 'error': 'Пароли не совпадают'}
                )
            user.set_password(new_pass)
            user.save()
            return redirect('profile')
        else:
            return HttpResponse('Error')


class ProductView(View):
    @staticmethod
    def get(request, pk):
        product = Product.objects.get(pk=pk)
        account = UserAccount.objects.get(account=product.user)
        images = ProductImage.objects.filter(product=product)
        if request.user.is_anonymous:
            favourite = False
        elif Favourite.objects.filter(user=request.user, product=product).exists():
            favourite = True
        else:
            favourite = False
        context = {
            'favourite': favourite,
            'CommentForm': CommentForm(),
            'comments': Comment.objects.filter(product=product),
            'account': account,
            'product': product,
            'images': images
        }
        return render(request, 'store/product_page.html', context)

    @staticmethod
    def post(request, pk):
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                comment=form.cleaned_data.get('comment'),
                product=Product.objects.get(pk=pk),
                user=request.user
            )
            return redirect(request.META['HTTP_REFERER'])
        else:
            return HttpResponse('error')


class ProductFavouriteHandler(View):
    @staticmethod
    @login_required(login_url=reverse_lazy('user_login'))
    def get(request, pk):
        favourite = Favourite.objects.filter(user=request.user, product_id=pk)
        if favourite.exists():
            favourite.delete()
        else:
            Favourite.objects.create(
                user=request.user,
                product_id=pk
            )
        return redirect(request.META['HTTP_REFERER'])
