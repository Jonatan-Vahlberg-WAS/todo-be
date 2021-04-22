from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ListSerializer, TaskSerializer
from .models import List,Task
from django.http import Http404
# Create your views here.

#GET

@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'List': '/api/lists/',
        'Detail View': '/api/lists/detail/<str:pk>/',
        'Create': '/api/lists/create/',
        'Update': '/api/lists/update/<str:pk>/',
        'Delete': '/api/lists/delete/<str:pk>/',
    }
    return Response(api_urls)

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
