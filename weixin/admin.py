from django.contrib import admin

# Register your models here.

from .models import UserInfo, Express, UserLocation


class UserLocationAdmin(admin.ModelAdmin):
    list_display = ('user', 'Latitude', 'Longitude', 'createTime')
    search_fields = ('user',)
    list_filter = ('user', 'createTime')
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('nickname','remark','openid','sex', 'country', 'language', 'city','subscribe_time','subscribe','headimgurl')
    search_fields = ('nickname','remark','openid')
    list_filter = ('nickname', 'sex')


# admin.site.register(User)
admin.site.register(UserInfo,UserInfoAdmin)
admin.site.register(Express)
admin.site.register(UserLocation, UserLocationAdmin)
