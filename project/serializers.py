from rest_framework import serializers
from .models import Project, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at']  # 'project' 필드 제외
        read_only_fields = ['id', 'created_at']  # 읽기 전용 필드 설정

    def create(self, validated_data):
        return super().create(validated_data)

class ProjectSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)  # 프로젝트에 연결된 댓글 목록을 포함

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['score']  # score 필드를 읽기 전용으로 설정


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'team_name', 'team_members', 'score']  # 목록 조회 시 필요한 필드만 선택
