from django.contrib import admin

from users.models import User, Subscription


class UserAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'username',
                    'first_name',
                    'last_name',
                    'password',
                    'email',
                    )
    list_filter = ('username', 'email')


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'subscriber',
                    'author',
                    )


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
