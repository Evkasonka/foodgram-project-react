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
    list_filter = ("name",)
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
        "author",
        "name",
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
    list_filter = ("ingredient",)
    search_fields = ("ingredient",)


class IsFavoritedAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "recipe",
    )
    list_filter = ("user",)
    search_fields = ("user",)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientAmountInRecipe, IngredientAmountInRecipeAdmin)
admin.site.register(IsFavorited, IsFavoritedAdmin)
