from rest_framework import serializers
import logging
import datetime
from .models import List, Task
from django.contrib.auth.models import User



class UserSerilizer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id','username','password')

    def create(self,validated_data):
        user = User.objects.create(
            username=validated_data['username'], 
            password=validated_data['password']
        )
        return user

class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Task
        fields = ('title', 'completed', 'id')
        read_only_fields = ('parent',)

class ListSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = List
        fields = ('title','updated_at','id','tasks')
    
    def create(self,validated_data):
        tasks = validated_data.pop('tasks')
        _list = List.objects.create(**validated_data)
        for task in tasks:
            print(task.keys())
            Task.objects.create(parent=_list, **task)
        return _list
    
    def update(self,instance,validated_data):
        tasks = validated_data.pop('tasks')
        instance.title = validated_data.get('title',instance.title)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)
        instance.save()

        keep_tasks = []
        exsisting_ids = [task.id for task in instance.tasks.all()]
        for task in tasks:
            if "id" in task.keys():
                if Task.objects.filter(id=task["id"]).exists():
                    t = Task.objects.get(id=task["id"])
                    t.title = task.get("title",t.title)
                    t.completed = task.get("completed",t.completed)
                    t.save()

                    keep_tasks.append(t.id)
                else:
                    continue
            else:
                t = Task.objects.create(parent=instance, **task)
                keep_tasks.append(t.id)
        
        for task in instance.tasks.all():
            if task.id not in keep_tasks:
                task.delete()

        return instance