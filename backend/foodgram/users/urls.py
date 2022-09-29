from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet, FollowViewSet, SubscribeViewSet


router = DefaultRouter()
router.register(
    'users/subscriptions',
    FollowViewSet,
    basename='subscriptions'
)
router.register(
    r'users/(?P<user_id>[\d]+)/subscribe',
    SubscribeViewSet,
    basename='subscribe'
)
router.register('users', CustomUserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    re_path(r'auth/', include('djoser.urls.authtoken')),
]
