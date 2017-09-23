from collections import OrderedDict

from rest_framework import serializers

from .models import Profile, User

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True, many=False, partial=True)

    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('id',)

    def create(self, validated_data: OrderedDict) -> Profile:
        user_validated_data = validated_data.pop('user')
        user = User.objects.create(**user_validated_data)

        return Profile.objects.create(user=user, **validated_data)

    def update(self, instance: Profile, validated_data: OrderedDict) -> Profile:
        user_data = validated_data.pop('user')
        user = instance.user

        profile_serializer = ProfileSerializer(instance, data=validated_data)
        user_serializer = UserSerializer(user, data=user_data)

        if user_serializer.is_valid():
            user_serializer.update(user, user_data)

        if profile_serializer.is_valid():
            #profile_serializer.update(instance, validated_data)
            pass

        instance.save()

        return instance
