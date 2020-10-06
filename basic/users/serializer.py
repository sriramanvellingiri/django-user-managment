from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # fields = ('id','first_name','last_name', 'email')
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('role', 'address', 'city', 'created_datetime', 'modified_datetime')


class UserListSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email','profile')

class UserCreateUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'profile','password')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        validated_data['username'] = validated_data.get('email') #overriding the username with email
        user,is_created = User.objects.get_or_create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        Profile.objects.create(user=user, **profile_data)
        return user

    def validate(self, data):
        """
        Check that start is before finish.
        """
        if data['first_name'] == 'userfour':
            raise serializers.ValidationError("User Four",code=400,detail={
                'first_name': 'Value in the first Name is invalid'
            })
        return data


    def update(self, instance, validated_data):
        try:
            profile_data = validated_data.pop('profile')
            profile = instance.profile
            instance.first_name = validated_data.get('first_name',instance.first_name)
            instance.last_name = validated_data.get('last_name',instance.last_name)
            instance.email = validated_data.get('email',instance.email)
            instance.save()
            profile.address = profile_data.get('address',profile.address)
            profile.city = profile_data.get('city',profile.city)
            profile.save()
            return instance
        except Exception as e:
            print(e)

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class LogoutSerializer(serializers.Serializer):
    pass