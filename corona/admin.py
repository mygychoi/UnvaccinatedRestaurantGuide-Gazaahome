from django.contrib import admin

from corona.models import Restaurant, RestaurantComment, RestaurantCategory, RestaurantTag, UnvaccinatedPass
from corona.models import Post, PostComment, PostCategory


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address', 'latitude', 'longitude', 'unvaccinated_pass', 'verifieded', 'created_at']
    list_display_links = ['id', 'name', ]


@admin.register(RestaurantComment)
class RestaurantCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'restaurant', 'is_anonymous', 'created_at']
    list_display_links = ['id', 'restaurant', ]


@admin.register(RestaurantCategory)
class RestaurantCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
    list_display_links = ['id', 'name', ]


@admin.register(UnvaccinatedPass)
class UnvaccinatedPassAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', ]
    list_display_links = ['id', 'type', ]


@admin.register(RestaurantTag)
class RestaurantTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
    list_display_links = ['id', 'name', ]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'is_anonymous', 'category', 'created_at']
    list_display_links = ['id', 'title', ]


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'is_anonymous', 'created_at']
    list_display_links = ['id', 'post', ]


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]
    list_display_links = ['id', 'name', ]