from django.urls import path
from .views import UserProfileList, UserProfileDetail, \
    RegistrationView, CustomLoginView, BusinessProfileList, \
    BusinessProfileDetail, CustomerProfileList, CustomerProfileDetail


urlpatterns = [     
    path('', UserProfileList.as_view(), name='userprofile-list'),
    path('profiles/', UserProfileList.as_view(), name='userprofile-list'),
    path('profiles/business/', BusinessProfileList.as_view(), name='businessprofile-list'),
    path('profiles/business/<int:pk>/', BusinessProfileDetail.as_view(), name='businessprofile-detail'),
    path('profiles/customer/', CustomerProfileList.as_view(), name='customerprofile-list'),
    path('profiles/customer/<int:pk>/', CustomerProfileDetail.as_view(), name='customerprofile-detail'),
    path('profile/<int:pk>/', UserProfileDetail.as_view(), name='userprofile-detail'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', CustomLoginView.as_view(), name='login'),
]
