from hashlib import new
from django.shortcuts import render

from usuario.models import CustomUsuario as User

from .serializers import NpSerializer


from rest_framework import viewsets, status
from rest_framework import serializers

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
from .models import NpData
import csv
import json
from io import TextIOWrapper

from django.core.files.base import ContentFile
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

import base64
import tempfile
from django.http import FileResponse


class NpViewSet(viewsets.ModelViewSet):
    queryset = NpData.objects.all()
    serializer_class = NpSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=["POST"])
    def get_data_np_project(self, request, pk=None):
        if request.user.is_authenticated:
            user_id = request.user.id
            user = User.objects.get(id=user_id)
            try:
                json_data = json.loads(request.body)

                # tmp = tempfile.NamedTemporaryFile(delete=False)
                # with open(tmp.name, "w") as fi:
                #     json.dump(json_data, fi)

                # new_file = NpData(nome="marcelo teste", user=user, arquivo=File())
                # new_file.save()

                response = {"data": json_data}
                return Response(response, status=status.HTTP_200_OK)
            except Exception as e:
                print(f"Error na Requisição {e}")
        else:
            response = {"message": "Você precisa estar logado!!!"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
