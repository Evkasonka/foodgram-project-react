from django.contrib import admin
from django.contrib.admin import display
from recipes.models import (Ingredient, IngredientAmountInRecipe, IsFavorited,
                            Recipe, Tag)


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "measurement_unit",
    )
    list_filter = ("measurement_unit",)
    search_fields = ("name",)


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "color",
        "slug",
    )
    list_filter = ("name",)
    search_fields = ("name",)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "name",
        "cooking_time",
        "add_in_favorites",
    )
    list_filter = (
        "tags",
    )
    search_fields = ("name",)

    @display(description="Число добавлений рецепта в избранное")
    def add_in_favorites(self, object):
        return object.favorites.count()


class IngredientAmountInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "ingredient",
        "recipe",
        "amount",
    )
    list_filter = ("recipe__tags",)
    search_fields = ("recipe__author__email",
                     "recipe__author__username",
                     "ingredient__name")


class IsFavoritedAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "recipe",
    )
    list_filter = ("recipe__tags",)
    search_fields = ("user__email",
                     "user__username",
                     "recipe__name")


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientAmountInRecipe, IngredientAmountInRecipeAdmin)
admin.site.register(IsFavorited, IsFavoritedAdmin)
