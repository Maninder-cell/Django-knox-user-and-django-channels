from django.shortcuts import render
from django.http import JsonResponse,Http404
from .models import Note
from .serializers import todoSerializer,userSerializer
from rest_framework import permissions,status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics,permissions
from rest_framework.decorators import api_view,action
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth.models import User
from rest.permissions import IsOwnerOrReadOnly
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.throttling import UserRateThrottle
# Create your views 
# class todoData(APIView):
#     def get(self,request):
#         queryset = Note.objects.all()
#         Serial_queryset = todoSerializer(queryset,many=True)
#         return Response(Serial_queryset.data)
        
#     def post(self,request):
#         data = todoSerializer(data=request.data)
#         if data.is_valid():
#             data.save()
#             return Response(data.data,status=status.HTTP_201_CREATED)
#         return Response(data.errors,status=status.HTTP_400_BAD_REQUEST)

# class todoData(
#                 mixins.ListModelMixin,
#                 mixins.CreateModelMixin,
#                 generics.GenericAPIView
#               ):
#     queryset = Note.objects.all()
#     serializer_class = todoSerializer

#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)

#     def post(self,request,*args,**kwargs):
#         return self.create(request,*args,**kwargs)

# class todoDataDetail(
#                 mixins.RetrieveModelMixin,
#                 mixins.UpdateModelMixin,
#                 mixins.DestroyModelMixin,
#                 generics.GenericAPIView
#               ):
#     queryset = Note.objects.all()
#     serializer_class = todoSerializer

#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request,*args,**kwargs)

#     def put(self,request,*args,**kwargs):
#         return self.update(request,*args,**kwargs)
    
    # def delete(self,request,*args,**kwargs):
    #     return self.delete(request,*args,**kwargs)
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('users', request=request, format=format),
        'Notes': reverse('todo', request=request, format=format)
    })
    
class todoDone(generics.ListAPIView):
    serializer_class = todoSerializer

    def get_queryset(self):
        state = self.request.query_params.get("state",None)
        return Note.objects.filter(done=state)

class todoData(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = todoSerializer
    throttle_classes = [UserRateThrottle]
    lookup_field = 'owner'
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    @action(detail=True,name='todo')
    def done(self,request, pk=None):
        print("hi")
        data = Note.objects.filter(done = True)
        return Response(data)

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        user = self.kwargs.get("owner",None)
        state = self.request.query_params.get("state",None)
        if state is not None:
            return Note.objects.filter(done=state)
        elif user:
            return Note.objects.filter(owner=User.objects.get(username=user))
        else:
            return Note.objects.all()
    
    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data=serializer.data)

# class todoDataDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Note.objects.all()
#     serializer_class = todoSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

class userData(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializer