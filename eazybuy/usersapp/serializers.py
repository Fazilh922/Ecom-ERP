from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import AuthenticationFailed

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username=username).first() or User.objects.filter(email=username).first()

        if user and user.check_password(password):
            return {
                'user': user,
                'tokens': self.generate_tokens(user),
            }
        raise AuthenticationFailed('Invalid credentials')

    def generate_tokens(self, user):
        # Implement token generation, e.g., using `rest_framework_simplejwt`
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])  # Hash password
        user.save()
        return user