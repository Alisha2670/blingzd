from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('shop/', views.shop, name='shop'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('index/', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_quantity/', views.update_quantity, name='update_quantity'),
    path('remove_item/<int:item_id>/', views.remove_item, name='remove_item'),
]
