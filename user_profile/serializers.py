from rest_framework import serializers
from .models import Profile#, Project, Board



class ProfileSerializer(serializers.ModelSerializer):
     school_id = serializers.IntegerField(required=False)
     name = serializers.CharField(required=False, allow_blank=True)
     code = serializers.CharField(required=False, allow_blank=True)
     password = serializers.CharField(required=False, allow_blank=True)
     range = serializers.CharField(required=False, allow_blank=True)

     class Meta:
        model = Profile
        fields = '__all__'
