from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as harsh_views
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('accounts/login', harsh_views.LoginView.as_view(template_name='harsh/login.html'), name='login'),
    path('accounts/logout', views.user_logout, name='logout'),
    path('accounts/details/', views.customer_details, name='details'),
    path('mobile/',views.mobile, name='mobile'),
    path('mobile/<slug:data>/', views.mobile, name='mobile'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/',views.cart, name='cart'),
    path('remove/<int:id>/',views.remove_from_cart, name='remove'),
    path('update/<int:id>/',views.update_quant, name='update'),
    path('place/',views.check, name='place'),
    path('giveorder/',views.place_order, name='giveorder'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)