from django.contrib import admin
from board.models import Board  # board 앱의 모델 가져오기
# Register your models here.
from .models import Profile#,Project,Board
# Register your models here.

admin.site.register(Profile)

# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('school_id', 'name', 'range', 'code')

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'id')
