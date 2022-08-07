from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import *


class PatientSerializer(serializers.ModelSerializer):

    sex = serializers.SerializerMethodField()
    allergies = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = '__all__'

    def get_sex(self, obj):
        return obj.get_sex_display()

    def get_allergies(self, obj):
        return obj.get_allergies_display()


class UserSerializer(serializers.ModelSerializer):

    patient = PatientSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'patient']



