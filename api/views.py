from django.shortcuts import render
from usuario.models import CustomUsuario as User

from .serializers import ValuRiskSerializer

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

import json
from django.http import JsonResponse
from django.core.serializers import serialize
from django.db.models import Q
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from decimal import *
from .models import ValuRisk
import csv


class ValuRiskViewSet(viewsets.ModelViewSet):
    queryset = ValuRisk.objects.all().order_by('data')
    serializer_class = ValuRiskSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['POST'])
    def save_risk(self,request,pk=None):
        if request.user.is_authenticated:
            if 'data_csv' in request.data:
                try:
                    file = request.FILES['data_csv']
                    user_id = request.user.id
                    user = User.objects.get(id=user_id)
                    decoded_file = file.read().decode('utf-8').splitlines()
                    reader = csv.reader(decoded_file)
                    next(reader)
                    count = 0
                    list_obj = []
                    for row in reader:
                        data_value = f'{row[0].split(".")[-1]}-{row[0].split(".")[-2]}-{row[0].split(".")[-3]}'
                        abertura = float(row[2].replace(',', '.'))
                        fechamento = float(row[1].replace(',', '.'))
                        maxima = float(row[3].replace(',', '.'))
                        minimo = float(row[4].replace(',', '.'))
                        if ValuRisk.objects.filter(data=data_value).exists():
                            print('Operação já registrada')
                        else:
                            nova_operacao = ValuRisk(
                                data = data_value,
                                abertura = abertura,
                                fechamento = fechamento,
                                minimo=minimo,
                                maxima=maxima,
                                user=user,
                            )
                            nova_operacao.save()
                            print('Operação salva!!!!!')
                            count += 1
                            atualizacao_dict = {'data' : data_value , 'valor': fechamento}
                            list_obj.append(atualizacao_dict)
                    qs = ValuRisk.objects.only('data', 'fechamento')
                    serializer = ValuRiskSerializer(qs, many=True)
                    quantidade_atualizada = count
                    print(list_obj)
                    response = {
                        'msg': f'Dados alterados com sucesso',
                        'quantidade_alterada' : quantidade_atualizada,
                        'atualizacao_dict' : list_obj,
                        'dados': serializer.data 
                    }

                    return Response(response, status=status.HTTP_200_OK)
                except Exception as e:
                    response = {'message': f'Ocorreu um Erro: {e}'}
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {'message': 'Você precisa enviar a imagem para atualizar'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {'message': 'Você precisa estar logado!!!'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def get_risks(self, request):
        if request.user.is_authenticated:
            try:
                startdate = datetime.today()                
                enddate = startdate - relativedelta(years=5)
                qs = ValuRisk.objects.filter(data__gte=enddate).order_by('data')
                # data = {
                #     'datas' : [x.data for x in qs],
                #     'values' : [x.fechamento for x in qs]
                # }
                new_list = []
                for i in qs:
                    if i.fechamento > 1:
                        new_dict = {
                            'x' : i.data,
                            'y' : i.fechamento
                        }
                        new_list.append(new_dict)
                

                # serializer = ValuRiskSerializer(qs, many=True)
                response = {'msg': f'Consulta realizada com sucesso!!', 'total_return' : len(new_list) ,'dados': new_list }
                return Response(response, status=status.HTTP_200_OK)
            except Exception as e:
                response = {'message': f'Ocorreu um Erro: {e}'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {'message': 'Você precisa estar logado!!!'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
