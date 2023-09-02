from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny,
                                        IsAuthenticatedOrReadOnly,
                                        IsAuthenticated,
                                        SAFE_METHODS)
from rest_framework.status import (HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT)
from recipes.models import (Ingredient,
                            IngredientAmountInRecipe,
                            IsFavorited,
                            IsInShoppingCart,
                            Recipe,
                            Tag,)
from api.serializers import (IngredientSerializer,
                             RecipeReadSerializer,
                             RecipeWriteSerializer,
                             TagSerializer,
                             RecipePreviewSerializer,
                             FavoriteSerializer,
                             ShoppingCartSerializer)
from api.permissions import AuthorOrReadOnly
from recipes.filters import (RecipeFilter,
                             IngredientSearchFilter)
from recipes.shopping_cart_to_pdf import generate_shopping_list_pdf


class IngredientViewSet(ReadOnlyModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientSearchFilter


class TagViewSet(ReadOnlyModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipeViewSet(ModelViewSet):

    queryset = Recipe.objects.all()
    serializer_class = RecipeWriteSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, AuthorOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @action(
        detail=True,
        methods=('post', 'delete',),
        url_path='favorite',
        url_name='favorite',
        permission_classes=(IsAuthenticated,)
    )
    def get_favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            serializer = FavoriteSerializer(
                data={'user': request.user.id,
                      'recipe': recipe.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            favorite_serializer = RecipePreviewSerializer(recipe)
            return Response(
                favorite_serializer.data, status=HTTP_201_CREATED
            )
        recipe_in_favorite = get_object_or_404(
            IsFavorited,
            user=request.user,
            recipe=recipe
        )
        recipe_in_favorite.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=('post', 'delete',),
        url_path='shopping_cart',
        url_name='shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
    def get_shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            serializer = ShoppingCartSerializer(
                data={'user': request.user.id,
                      'recipe': recipe.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            shopping_cart = RecipePreviewSerializer(recipe)
            return Response(
                shopping_cart.data,
                status=HTTP_201_CREATED
            )
        recipe_in_shopping_cart = get_object_or_404(
            IsInShoppingCart,
            user=request.user,
            recipe=recipe)
        recipe_in_shopping_cart.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=('get',),
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        ingredients = (IngredientAmountInRecipe.objects.filter(
                          recipe__shopping_cart__user=request.user).values(
                              'ingredient__name',
                              'ingredient__measurement_unit',).annotate(
                                  ingredient_sum=Sum('amount')))
        return generate_shopping_list_pdf(ingredients)
