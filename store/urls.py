from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    # Pages
    path('', views.IndexView.as_view(), name='index'),
    path('register/', cache_page(60*60*24)(views.RegisterUserView.as_view()), name='user_register'),
    path('login/', views.LoginUserView.as_view(), name='user_login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('changepass/', cache_page(60*60*24)(views.ChangePasswordUserView.as_view()), name='user_change_pass'),
    path('product/<int:pk>', views.ProductView.as_view(), name='product'),

    # Handlers
    path('handle/product/create', views.CreateProductHandler.as_view(), name='create_product_handler'),
    path('logout/', views.LogoutUserView.as_view(), name='user_logout'),
    path('favourite/<int:pk>', views.ProductFavouriteHandler.as_view(), name='product_favourite'),

    # AJAX
    path('v1/advertisements/get/', views.AdvertisementGetAJAX.as_view(), name='advertisements_get_ajax'),
    path('v1/advertisements/delete/<int:pk>', views.AdvertisementDeleteAJAX.as_view(), name='advertisements_delete_ajax')
]
