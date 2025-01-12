"""
URL configuration for coderr_backend_hub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from offers_app.api.views import OfferDetailView
from orders_app.api.views import OpenOrdersCountView, CompletedOrdersCountView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('users_auth_app.api.urls')),
    path('api/offers/', include('offers_app.api.urls')),
    path('api/offerdetails/<int:pk>/', OfferDetailView.as_view(), name='offer-detail', ),
    path('api/reviews/', include('reviews_app.api.urls')),
    path('api/orders/', include('orders_app.api.urls')),
    path('api/order-count/<int:business_user_id>/', OpenOrdersCountView.as_view(), name='open-orders-count'),
    path('api/completed-order-count/<int:business_user_id>/', CompletedOrdersCountView.as_view(), name='completed-orders-count'),
    path('api/base-info/', include('base_info_app.api.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
