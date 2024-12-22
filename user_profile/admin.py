# from django.contrib import admin
# from board.models import Board  # board 앱의 모델 가져오기
# # Register your models here.
# from .models import Profile#,Project,Board
# # Register your models here.

# admin.site.register(Profile)

# # @admin.register(Profile)
# # class ProfileAdmin(admin.ModelAdmin):
# #     list_display = ('school_id', 'name', 'range', 'code')

# @admin.register(Board)
# class BoardAdmin(admin.ModelAdmin):
#     list_display = ('title', 'content', 'id')


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profile" # 복수형으로 이름 표기하지 않도록 직접 지정
    
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)