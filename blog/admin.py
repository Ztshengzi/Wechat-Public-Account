from django.contrib import admin
# Register your models here.
from .models import Post, Category, Tag

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','excerpt','modified_time','flag')
    search_fields = ('title',)
    list_filter = ('title','modified_time')
admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)

