from rest_framework import serializers
from .models import Project, Comment

# 댓글 모델에 대한 Serializer
# 특정 프로젝트에 연결된 댓글 정보를 처리하거나 조회할 때 사용
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at']  # 댓글의 ID, 내용, 생성 일시만 반환
        read_only_fields = ['id', 'created_at']  # 읽기 전용 필드 설정

    def create(self, validated_data):
        # 기본 생성 메서드 활용
        return super().create(validated_data)


# 프로젝트 모델에 대한 상세 Serializer
# 프로젝트의 모든 필드와 해당 프로젝트에 연결된 댓글을 포함하여 반환
class ProjectSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)  # 프로젝트에 연결된 댓글 목록 포함

    class Meta:
        model = Project
        fields = '__all__'  # 프로젝트의 모든 필드를 반환
        read_only_fields = ['score']  # score는 읽기 전용 필드로 설정


# 프로젝트 목록 조회용 Serializer
# 프로젝트의 간단한 정보(팀명, 팀원, 점수)만 반환
class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'team_name', 'team_members', 'score']  # 목록 조회 시 필요한 필드만 반환
