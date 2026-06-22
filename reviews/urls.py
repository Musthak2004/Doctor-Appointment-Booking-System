from django.urls import path

from .views import (
    ReviewCreateView,
    ReviewDetailView,
    ReviewListView,
)

app_name = "reviews"

urlpatterns = [

    path(
        "",
        ReviewListView.as_view(),
        name="review_list"
    ),

    path(
        "create/<int:appointment_id>/",
        ReviewCreateView.as_view(),
        name="review_create"
    ),

    path(
        "<int:pk>/",
        ReviewDetailView.as_view(),
        name="review_detail"
    ),
]
