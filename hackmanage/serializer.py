from rest_framework import serializers
from hackmanage.models import *
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(
        write_only=True,  # Password is write-only to avoid returning it in the response
        required=True,    # Make password required
        style={'input_type': 'password'}  # To show password in a password field if needed (useful for rendering forms)
    )

    def validate(self, data):
        # Optionally, you can add extra validation logic here
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Username and password are required.")
        
        return data



class ListHackathonSerializer(serializers.ModelSerializer):
  class Meta:
    model = Hackathon
    fields = '__all__'

class CreateHackathonSerializer(serializers.ModelSerializer):
  class Meta:
    model = Hackathon
    exclude = ['hack_id','created_at','updated_at','started_at','ended_at','is_active', 'user']
    # fields = ['tittle','description','reward_price','hackathon_submission_type']


class SubmissionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Submission
    fields = '__all__'



class CreateSubmissionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Submission
    fields = ['description','user_submission_type','user_submission', 'hackathon']


