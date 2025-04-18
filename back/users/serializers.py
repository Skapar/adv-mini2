from rest_framework import serializers
from .models import CustomUser
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_url = reverse('verify-email', kwargs={'uidb64': uid, 'token': token})
        full_url = f"http://localhost:8000{verification_url}"

        send_mail(
            'Verify your email',
            f'Please click this link to verify your email: {full_url}',
            None,
            [user.email],
            fail_silently=False,
        )
        return user


class PasswordResetSerializer(serializers.Serializer):
    username = serializers.CharField()
    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        current_password = data.get('current_password')

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this username does not exist")

        if not user.check_password(current_password):
            raise serializers.ValidationError("Current password is incorrect")

        return data

    def save(self):
        username = self.validated_data['username']
        new_password = self.validated_data['new_password']
        user = CustomUser.objects.get(username=username)
        user.set_password(new_password)
        user.save()
        return user