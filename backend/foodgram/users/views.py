from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, status, mixins

from users.serializers import FollowerSerializer, FollowCreateSerializer
from users.models import Subscribe


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    pagination_class = PageNumberPagination


class FollowViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowerSerializer

    def get_queryset(self):
        return self.request.user.subscriptions.all()


class SubscribeViewSet(viewsets.GenericViewSet,
                       mixins.CreateModelMixin, mixins.DestroyModelMixin):
    serializer_class = FollowCreateSerializer

    def get_queryset(self):
        return get_object_or_404(
            User, id=self.kwargs.get('user_id')
        )

    def create(self, request, user_id):
        user = request.user
        author = get_object_or_404(User, id=user_id)
        if user == author:
            return Response(
                'Нельзя подписаться на себя',
                status=status.HTTP_400_BAD_REQUEST
            )
        if Subscribe.objects.filter(user=user, author=author).exists():
            return Response(
                'Такая подписка уже существует',
                status=status.HTTP_400_BAD_REQUEST
            )
        follow = Subscribe.objects.create(user=user, author=author)
        serializer = FollowerSerializer(
            follow.author, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id, format=None):
        author = get_object_or_404(
            User, id=user_id
        )
        try:
            subscribe = get_object_or_404(
                Subscribe,
                user=self.request.user,
                author=author
            )
        except NameError:
            msg = f'Автор {author} отсутствут в Ваших подписках.'
            return Response(
                {'errors': msg}, status=status.HTTP_400_BAD_REQUEST
            )
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
