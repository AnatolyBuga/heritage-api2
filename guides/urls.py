from django.urls import path
from rest_framework.routers import DefaultRouter
from guides import views

router = DefaultRouter()
router.register('friendly_tags', views.FriendlyTagViewSet, basename='friendly_tag')

urlpatterns = [
    # path('place/', views.PlaceView.as_view(), name='place'),
    # path('place/<place_id>', views.PlaceView.as_view(), name='place')
]

urlpatterns += router.urls