# pylint: disable=E1101
from .models import Memo
from rest_framework import serializers


class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = ('title', 'text')

    def create(self, validated_data):
        return Memo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance
