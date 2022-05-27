from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import ValuRisk
from rest_framework.fields import CurrentUserDefault

from usuario.models import CustomUsuario as User

class ValuRiskSerializer(serializers.ModelSerializer):    

    class Meta:
        model = ValuRisk
        fields = '__all__'
    
    



