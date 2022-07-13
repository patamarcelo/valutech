from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import NpData
from rest_framework.fields import CurrentUserDefault

from usuario.models import CustomUsuario as User

class NpSerializer(serializers.ModelSerializer):    

    class Meta:
        model = NpData
        fields = '__all__'
    
    



