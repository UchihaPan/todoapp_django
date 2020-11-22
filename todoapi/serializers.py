from rest_framework import serializers
from todo.models import Todo


class Todocompletedserializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    datecompleted = serializers.ReadOnlyField()

    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'created', 'datecompleted', 'important']


class Todocompleteserializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id']
        read_only_fields = ['title', 'description', 'created', 'datecompleted', 'important']