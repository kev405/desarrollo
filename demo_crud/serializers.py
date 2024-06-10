from rest_framework import serializers
from .models import CustomUser
from .models import CustomWorkManagement
from .models import CustomJobManagement
from .models import CustomProgressManagement

#User
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password','name', 'phone', 'role', 'is_active', 'is_staff']


class CustomWorkManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomWorkManagement
        fields = ['id', 'nombre', 'direccion', 'director', 'capataz', 'peones', 'ayudantes','estado','reporte']


class CustomJobManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomJobManagement
        fields = ['id', 'nombre', 'obra', 'director', 'capataz', 'peones', 'ayudantes', 'estado','reporte']




class CustomProgressManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomProgressManagement
        fields = ['id', 'obra', 'latitud', 'longitud', 'tareas', 'observaciones', 'nota_de_voz']


