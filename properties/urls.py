from django.urls import path
from .views import PropertyView, PropertyDetailView

urlpatterns = [
    path('/', PropertyView.as_view(), name='property-list'),
    path('/<str:id>', PropertyDetailView.as_view(), name='property-detail-view'),
]
