from django.contrib import admin
from .models import Like, Post,BlogComment

# Register your models here.
# admin.site.register(Post)
admin.site.register(BlogComment)
admin.site.register(Like)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass