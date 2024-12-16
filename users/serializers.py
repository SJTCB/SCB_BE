from .models import CustomUser  # CustomUser 모델을 가져옵니다
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate

# 회원가입 시리얼라이저
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())],  # CustomUser로 변경
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],  # 비밀번호 검증
    )
    password2 = serializers.CharField(  # 비밀번호 확인 필드
        write_only=True,
        required=True,
    )
    school_id = serializers.CharField(  # 학번 추가 (중복 검사 필요)
        required=False,  # 선택적 입력
        validators=[UniqueValidator(queryset=CustomUser.objects.all())],  # CustomUser로 변경
    )
    range = serializers.CharField(  # 분야 추가
        required=False,  # 선택적 입력
    )
    code = serializers.CharField(  # 코드 추가
        required=False,  # 선택적 입력
    )

    class Meta:
        model = CustomUser  # 모델을 CustomUser로 변경
        fields = ('username', 'email', 'password', 'password2', 'school_id', 'range', 'code')

    def validate(self, data):
        # password와 password2의 일치 여부 확인
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        
        return data

    def create(self, validated_data):
        # CREATE 요청에 대해 create 메서드를 오버라이딩하여, 유저를 생성하고 토큰도 생성
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        # school_id, range, code가 있을 경우에만 저장
        if 'school_id' in validated_data:
            user.school_id = validated_data['school_id']  # CustomUser에 school_id 저장
        
        if 'range' in validated_data:
            user.range = validated_data['range']  # CustomUser에 range 저장
        
        if 'code' in validated_data:
            user.code = validated_data['code']  # CustomUser에 code 저장
        
        user.set_password(validated_data['password'])
        user.save()
        
        token = Token.objects.create(user=user)
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    # write_only=True 옵션을 통해 클라이언트->서버의 역직렬화는 가능하지만, 서버->클라이언트 방향의 직렬화는 불가능하도록 해준다.
    
    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user) # 해당 유저의 토큰을 불러옴
            return token
        raise serializers.ValidationError( # 가입된 유저가 없을 경우
            {"error": "Unable to log in with provided credentials."}
        )