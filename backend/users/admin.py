from django.contrib import admin
from users.models import Subscription, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "password",
        "email",
    )
    list_filter = ("is_admin",)
    search_fields = ("username", "email")


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subscriber",
        "author",
    )
    search_fields = ("subscriber__username",
                     "subscriber__email",
                     "author__username",
                     "author__email",
                     )


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
