from rest_framework import serializers
from .models import Users, Apartaments, Manager
from django.contrib.auth import authenticate


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class ApartamentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Apartaments
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email", "")
        password = data.get("password", "")

        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "Пользователь деактивирован."
                    raise serializers.ValidationError(msg)
            else:
                msg = "Невозможно войти с предоставленными учетными данными."
                raise serializers.ValidationError(msg)
        else:
            msg = "Должны быть предоставлены адрес электронной почты и пароль."
            raise serializers.ValidationError(msg)
        return data
