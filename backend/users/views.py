from api.serializers import (CustomUserSerializer,
                             SubscriptionDisplaySerializer,
                             SubscriptionSerializer)
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from users.models import Subscription, User


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    filter_backends = (SearchFilter,)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CustomUserSerializer
    http_method_names = (
        "get",
        "post",
        "patch",
        "delete",
    )

    @action(
        detail=True,
        methods=(
            "post",
            "delete",
        ),
        url_path="subscribe",
        url_name="subscribe",
        permission_classes=(IsAuthenticated,),
    )
    def get_subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        if request.method == "POST":
            serializer = SubscriptionSerializer(
                data={"subscriber": request.user.id, "author": author.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            author_serializer = SubscriptionDisplaySerializer(
                author, context={"request": request}
            )
            return Response(
                author_serializer.data,
                status=status.HTTP_201_CREATED)
        subscription = get_object_or_404(
            Subscription, subscriber=request.user, author=author
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=("get",),
        url_path="subscriptions",
        url_name="subscriptions",
        permission_classes=(IsAuthenticated,),
    )
    def get_subscriptions(self, request):
        authors = User.objects.filter(author__subscriber=request.user)
        paginator = PageNumberPagination()
        result_pages = paginator.paginate_queryset(
            queryset=authors, request=request)
        serializer = SubscriptionDisplaySerializer(
            result_pages, context={"request": request}, many=True
        )
        return paginator.get_paginated_response(serializer.data)
