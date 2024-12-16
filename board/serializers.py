

from rest_framework import serializers
from .models import Board, Comment

# 댓글 데이터를 처리하는 Serializer
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'created_at']  # 댓글 ID, 내용, 작성자, 생성 시간 포함
        read_only_fields = ['created_at']  # 작성 시간은 읽기 전용
        ref_name = "BoardComment"  # 고유한 참조 이름 설정



# Board 생성 시 사용되는 Serializer
class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['school_id', 'title', 'content']  # 학번, 제목, 내용 포함
        read_only_fields = ['date_created', 'date_updated']  # 작성일과 수정일은 읽기 전용


# Board 수정 시 사용되는 Serializer
class BoardUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['title', 'content']  # 수정 가능한 필드만 포함


# Board 목록 조회 시 사용되는 Serializer
class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'school_id', 'title', 'date_created']  # 목록 조회용 간략 필드


# Board 상세 조회 시 사용되는 Serializer
class BoardDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)  # 관련 댓글 포함

    class Meta:
        model = Board
        fields = [
            'id',
            'school_id',
            'title',
            'content',
            'date_created',
            'date_updated',
            'comments',
        ]
        read_only_fields = ['date_created', 'date_updated', 'comments']
