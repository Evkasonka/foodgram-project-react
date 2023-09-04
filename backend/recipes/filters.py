from django_filters import rest_framework

from recipes.models import Ingredient, Recipe


class IngredientSearchFilter(rest_framework.FilterSet):
    name = rest_framework.CharFilter(lookup_expr="istartswith")

    class Meta:
        model = Ingredient
        fields = ("name",)


class RecipeFilter(rest_framework.FilterSet):
    author = rest_framework.CharFilter(field_name="author__id", method="filter_author")

    tags = rest_framework.AllValuesMultipleFilter(field_name="tags__slug")

    is_favorited = rest_framework.BooleanFilter(method="get_is_favorited")

    is_in_shopping_cart = rest_framework.BooleanFilter(method="get_is_in_shopping_cart")

    class Meta:
        model = Recipe
        fields = (
            "author",
            "tags",
            "is_favorited",
            "is_in_shopping_cart",
        )

    def filter_author(self, queryset, *args):
        user = self.request.query_params.get("author")
        if user == "me":
            return queryset.filter(author=self.request.user)
        return queryset.filter(author_id=user)

    def get_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset
