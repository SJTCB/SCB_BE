from rest_framework import serializers
from .models import Project, Comment
import base64

# 댓글 데이터를 처리하는 Serializer
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at']  # 댓글 ID, 내용, 생성 시간 포함
        read_only_fields = ['created_at']  # 작성 시간은 읽기 전용


# Project 생성 시 사용되는 Serializer
class ProjectSerializer(serializers.ModelSerializer):
    code_file = serializers.FileField(write_only=True, required=True)  # 생성 시에만 필요한 필드

    class Meta:
        model = Project
        fields = ['team_name', 'team_members', 'comment', 'code_file']  # 수정 시 code_file 제거
        read_only_fields = ['score', 'code']  # score와 code는 읽기 전용

    def create(self, validated_data):
        # code_file 데이터를 바이너리로 변환해 code 필드에 저장
        code_file = validated_data.pop('code_file')
        validated_data['code'] = code_file.read()  # BinaryField에 파일 데이터 저장
        validated_data['score'] = 0  # 기본 score 값 설정
        return super().create(validated_data)


# Project 수정 및 상세 조회에 사용되는 Serializer
class ProjectUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['team_name', 'team_members', 'comment']  # code_file 필드 제거


# Project 목록 조회 시 사용되는 Serializer
class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'team_name', 'team_members', 'score', 'comment']  # code 필드 제외


# Project 상세 조회 시 사용되는 Serializer (code 포함)
class ProjectDetailSerializer(serializers.ModelSerializer):
    code = serializers.SerializerMethodField()  # base64로 인코딩된 code 필드 추가
    comments = CommentSerializer(many=True, read_only=True)  # 연결된 댓글 목록 포함

    class Meta:
        model = Project
        fields = ['id', 'team_name', 'team_members', 'comment', 'score', 'code', 'comments']  # code 및 comments 포함

    def get_code(self, obj):
        # obj.code가 바이너리 데이터인 경우 base64로 인코딩하여 반환
        if obj.code:
            full_code = base64.b64encode(obj.code).decode('utf-8')
            return full_code[:50] + "..." if len(full_code) > 50 else full_code  # 최대 50글자 표시
        return None
