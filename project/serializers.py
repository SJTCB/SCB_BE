from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['score']  # score 필드를 읽기 전용으로 설정


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'team_name', 'team_members', 'score']  # 목록 조회 시 필요한 필드만 선택
