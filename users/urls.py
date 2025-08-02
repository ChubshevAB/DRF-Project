from django.urls import path

from .apps import UsersConfig
from .views import (
    PaymentListAPIView,
    PaymentCreateAPIView,
    PaymentRetrieveAPIView,
    PaymentUpdateAPIView,
    PaymentDestroyAPIView
)


app_name = UsersConfig.name


urlpatterns = [
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),
    path('payments/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('payments/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment-detail'),
    path('payments/<int:pk>/update/', PaymentUpdateAPIView.as_view(), name='payment-update'),
    path('payments/<int:pk>/delete/', PaymentDestroyAPIView.as_view(), name='payment-delete'),
]
