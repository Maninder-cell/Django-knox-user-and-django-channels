from rest_framework.serializers import ModelSerializer,HyperlinkedModelSerializer
from rest_framework import serializers
from .models import Note
from django.contrib.auth.models import User

class todoSerializer(ModelSerializer):
    owner = serializers.HyperlinkedRelatedField(view_name="user_detail",read_only=True,many=False)

    class Meta:
        model = Note
        fields = ["title","description","done","owner"]

    def validate(self,data):
        if data['title'] != "ui":
            raise serializers.ValidationError("something wrong")
        else:
            return data

class userSerializer(ModelSerializer):
    notes = serializers.HyperlinkedRelatedField(many=True,view_name="todo_detail",read_only=True)

    class Meta:
        model = User
        fields = ["id","username","notes"]