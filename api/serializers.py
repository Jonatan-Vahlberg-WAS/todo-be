from rest_framework import serializers
import datetime
from .models import List, Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'completed', 'id')
        depth = 1

class ListSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = List
        fields = ('title','updated_at','id','tasks')
    
    def create(self,validated_data):
        print(validated_data)
        tasks_data = validated_data.pop('tasks')
        _list = List.objects.create(**validated_data)
        for task_data in tasks_data:
            Task.objects.create(parent=_list, **task_data)
        return _list
    
    def update(self,instance,validated_data):
        # tasks_data = validated_data.pop('tasks')
        # tasks = (instance.tasks).all()
        # tasks = list(tasks)
        instance.title = validated_data.get('title', instance.title)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)
        instance.save()

        task_ids = [item['id'] for item in validated_data["tasks"]]
        for task in instance.tasks:
            if task.id not in task_ids:
                task.delete()

        for item in validated_data['tasks']:
            task = Task( title=item["title"],completed=item["completed"], parent=instance)
            task.save()

        return instance