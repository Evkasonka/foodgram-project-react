from django.core.validators import MinValueValidator
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from foodgram.settings import MIN_INGREDIENTS_AMOUNT, MIN_RECIPE_COOKING_TIME
from foodgram.validators import validate_username
from recipes.models import (Ingredient, IngredientAmountInRecipe, IsFavorited,
                            IsInShoppingCart, Recipe, Tag)
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator
from users.models import Subscription, User


class CustomUserSerializer(UserSerializer):
    is_subscribed = SerializerMethodField(
        read_only=True, method_name="get_is_subscribed"
    )

    class Meta:
        model = User
        fields = ("email", "id", "username", "first_name",
                  "last_name", "is_subscribed")

    def get_is_subscribed(self, object):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return object.author.filter(subscriber=request.user).exists()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ("email", "id", "username", "first_name",
                  "last_name", "password")
        extra_kwargs = {"password": {"write_only": True}}


class SubscriptionSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = "__all__"
        validators = (
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=("author", "subscriber"),
                message="Вы уже подписаны на данного автора",
            ),
        )


class InRecipeSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class SubscriptionDisplaySerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField(method_name="get_recipes")
    recipes_count = serializers.SerializerMethodField(
        method_name="get_recipes_count")

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_recipes_count(self, object):
        return object.recipes.count()

    def get_recipes(self, obj):
        request = self.context.get("request")
        limit = request.GET.get("recipes_limit")
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[: int(limit)]
        serializer = RecipePreviewSerializer(
            recipes, many=True, read_only=True)
        return serializer.data


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(
        required=True, max_length=150, validators=(validate_username,)
    )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True, max_length=150, validators=(validate_username,)
    )
    confirmation_code = serializers.CharField(required=True, max_length=150)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientAmountInRecipe
        fields = ("id", "amount")


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit")

    class Meta:
        model = IngredientAmountInRecipe
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = SerializerMethodField(method_name="get_ingredients")
    is_favorited = SerializerMethodField(
        read_only=True, method_name="get_is_favorited")
    is_in_shopping_cart = SerializerMethodField(
        read_only=True, method_name="get_is_in_shopping_cart"
    )

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_ingredients(self, object):
        ingredients = object.ingredient_amount_in_recipe.all()
        return IngredientInRecipeSerializer(ingredients, many=True).data

    def get_is_favorited(self, object):
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        return request.user.favorites.filter(recipe=object).exists()

    def get_is_in_shopping_cart(self, object):
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        return request.user.shopping_cart.filter(recipe=object).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(many=True)
    image = Base64ImageField(use_url=True, max_length=None)
    cooking_time = serializers.IntegerField(
        validators=(
            MinValueValidator(
                MIN_RECIPE_COOKING_TIME,
                message=f"Время приготовления должно быть "
                f"больше {MIN_RECIPE_COOKING_TIME}.",
            ),
        )
    )

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def validate_ingredients(self, ingredients):
        ingredients_data = [ingredient.get("id") for ingredient in ingredients]
        if len(ingredients_data) != len(set(ingredients_data)):
            raise ValidationError(
                [{"name": ["Рецепт с таким название уже существует."]}])
        for ingredient in ingredients:
            if int(ingredient.get("amount")) < MIN_INGREDIENTS_AMOUNT:
                raise ValidationError(
                    f"Количество ингредиента должно быть "
                    f"не меньше {MIN_INGREDIENTS_AMOUNT}"
                )
        return ingredients

    def validate_tags(self, tags):
        if len(tags) != len(set(tags)):
            raise ValidationError(
                "Теги рецепта не должны провторяться"
            )
        return tags

    @staticmethod
    def add_ingredients(ingredients_data, recipe):
        IngredientAmountInRecipe.objects.bulk_create(
            (
                IngredientAmountInRecipe(
                    ingredient=ingredient.get("id"),
                    recipe=recipe,
                    amount=ingredient.get("amount"),
                )
                for ingredient in ingredients_data
            ),
        )

    def create(self, validated_data):
        author = self.context.get("request").user
        tags_data = validated_data.pop("tags")
        ingredients_data = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags_data)
        self.add_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        recipe = instance
        instance.image = validated_data.get("image", instance.image)
        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.name)
        instance.cooking_time = validated_data.get(
            "cooking_time", instance.cooking_time
        )
        instance.tags.clear()
        instance.ingredients.clear()
        tags_data = validated_data.get("tags")
        instance.tags.set(tags_data)
        ingredients_data = validated_data.get("ingredients")
        IngredientAmountInRecipe.objects.filter(recipe=recipe).delete()
        self.add_ingredients(ingredients_data, recipe)
        instance.save()
        return instance

    def to_representation(self, recipe):
        serializer = RecipeReadSerializer(recipe)
        return serializer.data


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = IsFavorited
        fields = "__all__"
        validators = (
            UniqueTogetherValidator(
                queryset=IsFavorited.objects.all(),
                fields=("user", "recipe"),
                message="Этот рецепт уже в избранном",
            ),
        )


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = IsInShoppingCart
        fields = "__all__"
        validators = (
            UniqueTogetherValidator(
                queryset=IsInShoppingCart.objects.all(),
                fields=("user", "recipe"),
                message="Этот рецепт уже в списоке покупок",
            ),
        )


class RecipePreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")
