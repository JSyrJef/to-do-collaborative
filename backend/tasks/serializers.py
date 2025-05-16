from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task

# Serializer for User model
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password'] 
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

# Serializer for Collaborator atribute
class CollaboratorSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

# Serializer for Task model
class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='user.username')
    collaborators = serializers.SlugRelatedField(
        many=True, 
        slug_field='username',
        queryset=User.objects.all(),
        required=False
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'created_at', 'updated_at', 'owner', 'collaborators']
        read_only_fields = ['id','created_at', 'updated_at', 'owner']

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("El título debe tener al menos 3 caracteres.")
        return value
        
    def validate_status(self, value):
        if value not in [choice[0] for choice in Task.STATUS_CHOICES]:
            raise serializers.ValidationError(f"El estado debe ser uno de: {', '.join([choice[0] for choice in Task.STATUS_CHOICES])}")
        return value