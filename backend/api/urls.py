from django.urls import include, path
from recipes.views import IngredientViewSet, RecipeViewSet, TagViewSet
from rest_framework import routers
from users.views import CustomUserViewSet

app_name = "api"
router = routers.DefaultRouter()
router.register("users", CustomUserViewSet, basename="users")
router.register("tags", TagViewSet, basename="tags")
router.register("ingredients", IngredientViewSet, basename="ingredients")
router.register("recipes", RecipeViewSet, basename="recipes")

urlpatterns = [
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
