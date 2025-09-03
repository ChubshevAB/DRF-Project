from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .apps import UsersConfig
from .views import (
    UserCreateAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
    UserDestroyAPIView,
    PaymentListAPIView,
    PaymentCreateAPIView,
    PaymentRetrieveAPIView,
    PaymentUpdateAPIView,
    PaymentDestroyAPIView,
    MyTokenObtainPairView,
)


app_name = UsersConfig.name

urlpatterns = [
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserCreateAPIView.as_view(), name="user-register"),
    path("users/", UserListAPIView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserRetrieveAPIView.as_view(), name="user-detail"),
    path("users/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", UserDestroyAPIView.as_view(), name="user-delete"),
    path("payments/", PaymentListAPIView.as_view(), name="payment-list"),
    path("payments/create/", PaymentCreateAPIView.as_view(), name="payment-create"),
    path("payments/<int:pk>/", PaymentRetrieveAPIView.as_view(), name="payment-detail"),
    path(
        "payments/<int:pk>/update/",
        PaymentUpdateAPIView.as_view(),
        name="payment-update",
    ),
    path(
        "payments/<int:pk>/delete/",
        PaymentDestroyAPIView.as_view(),
        name="payment-delete",
    ),
]
