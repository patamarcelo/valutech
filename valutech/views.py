from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'first_name' : user.first_name.title(),
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            # 'image': request.build_absolute_uri(user.image.url),
            'last_name' : user.last_name.title(),
            'api_key': user.api_key,
            'api_secret' : user.api_secret,
        })