from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from user_app.api.serializers import RegisterSerializers
from rest_framework.authtoken.models import Token
from user_app import models
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
@api_view(['POST',])
@authentication_classes([TokenAuthentication])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegisterSerializers(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['username'] = account.username
            data['email'] = account.email
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data =  serializer.errors
        return Response(data)
    