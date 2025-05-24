from rest_framework import serializers
from .models import Dyscyplina, Kategoria
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import ZakladyUzytkownika

class DyscyplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dyscyplina
        fields = ['id', 'name']

class KategoriaSerializer(serializers.ModelSerializer):
    dyscypliny = serializers.SerializerMethodField()

    class Meta:
        model = Kategoria
        fields = ['id', 'name', 'dyscypliny']

    def get_dyscypliny(self, obj):
        return DyscyplinaSerializer(obj.dyscyplina_set.all(), many=True).data

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password2": "Hasła nie są takie same."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user


class ZakladUzytkownikaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZakladyUzytkownika
        fields = ['id', 'wartosc', 'wynik', 'stworzono']