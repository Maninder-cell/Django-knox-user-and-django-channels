from rest_framework import generics,permissions,response
from knox.models import AuthToken
from .serializers import RegisterSerialzer,UserSerializer,LogInSerializer

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerialzer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return response.Response({
            "user" : UserSerializer(user,context=self.get_serializer_context()).data,
            "token" : AuthToken.objects.create(user)[1]
        })

class LogInApi(generics.GenericAPIView):
    serializer_class = LogInSerializer

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data
        return response.Response({
            "user" : UserSerializer(user,context=self.get_serializer_context()).data,
            "token" : AuthToken.objects.create(user)[1]
        })

class UserApi(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user