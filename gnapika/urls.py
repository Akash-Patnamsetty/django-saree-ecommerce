"""
URL configuration for gnapika project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('product/<int:id>/', views.product_detail, name="product_details"),
    path('cart/', views.cart_view, name="cart"),
    path('like_view/', views.like_view, name="like_view"),
    path("login/",views.login_view,name="login"),
    path("signup/",views.signup_view,name="signup"),
    path("logout/",views.logout_view,name="logout"),
    path('test/',views.test_view,name="test"),
    path('profile/', views.profile_view, name="profile"),
    path('like/<int:product_id>/', views.like_product, name='like_product'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart_qty/<int:product_id>/', views.update_cart_qty, name='update_cart_qty'),
    path('order/cart/', views.order_from_cart, name='order_from_cart'),
    path('order/buy/<int:product_id>/', views.buy_now_order, name='buy_now_order'),
    path('search-results/', views.search_results, name='search_results'),
    path('load-more-products/', views.load_more_products, name='load_more_products'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path("save-address/", views.save_address, name="save_address"),
    path("create-payment/",views.create_payment,name="create-payment"),
    path("create-cod-order/", views.create_cod_order),
    path("order-success/", views.order_success),
    path("order_history/",views.orders_history,name="order_history"),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('search/', views.search_products, name='search_products'),
    path("dashboard-upload/", views.dashboard_upload, name="dashboard_upload"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

