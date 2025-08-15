from django.urls import path
from rest_framework.routers import SimpleRouter
from materials.views import (
    SubscriptionAPIView,
    PaymentAPIView,
)
from materials.views import (
    CourseViewSet,
    LessonListAPIView,
    LessonCreateAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    LessonDestroyAPIView,
)
from materials.apps import MaterialsConfig
from django.http import HttpResponse

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lessons_retrieve"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lessons_create"),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lessons_update"),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lessons_delete"),
    path('subscriptions/', SubscriptionAPIView.as_view(), name='subscriptions'),
    path('courses/<int:course_id>/payment/', PaymentAPIView.as_view(), name='course-payment'),
    path('payment/success/', lambda request: HttpResponse("Payment successful!"), name='payment-success'),
    path('payment/cancel/', lambda request: HttpResponse("Payment canceled."), name='payment-cancel'),
]

urlpatterns += router.urls
