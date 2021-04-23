from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerilizer, ListSerializer, TaskSerializer
from .models import List,Task
from django.http import Http404
# Create your views here.



@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def api_overview(request):
    api_urls = {
        'POST: Create user': '/api/user/create',
        'POST: Obtain Token':'/api/token/',
        'POST: Refresh Token':'/api/token/refresh/',
        '':'',
        'GET: List': '/api/lists/',
        'GET: Detail View': '/api/lists/detail/<str:pk>/',
        'POST: Create': '/api/lists/create/',
        'PUT: Update': '/api/lists/update/<str:pk>/',
        'DELETE: Delete': '/api/lists/delete/<str:pk>/',
        '':'',
    }
    return Response(api_urls)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def create_user(request):
    serializer = UserSerilizer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET'])
def get_lists(request):
    lists = List.objects.filter(user=request.user).all()
    serializer = ListSerializer(lists, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_list(request, pk):
    try:
        list_item = List.objects.filter(user=request.user).get(id=pk)
        serializer = ListSerializer(list_item, many=False)
        return Response(serializer.data)
    except List.DoesNotExist:
        raise Http404

@api_view(['POST'])
def create_list(request):
    serializer = ListSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user = request.user)
    return Response(serializer.data)

@api_view(['PUT'])
def update_list(request, pk):
    try:
        list_item = List.objects.filter(user=request.user).get(id=pk)
        serializer = ListSerializer(instance=list_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    except List.DoesNotExist:
        raise Http404

@api_view(['DELETE'])
def delete_list(request, pk):
    
    try:
        list_item = List.objects.filter(user=request.user).get(id=pk)
        list_item.delete()
        return Response("List deleted successfully")
    except List.DoesNotExist:
        raise Http404
