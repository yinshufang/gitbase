from django.contrib.auth.models import User
from rest_framework import serializers
from snippets.models import Snippet


# class SnippetSerializer(serializers.Serializer):
class SnippetSerializer(serializers.ModelSerializer):
    # 控制显示模板
    # id = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    # code = serializers.CharField(style={'base_template': 'textarea.html'})

    # source参数就指定了哪个属性用于填充字段，为了在使用的时候显示owner，
    # 但是还要把它添加进Meta类里面
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        # 数据库以及显示的字段
        model = Snippet
        fields = ('id', 'title', 'code', 'owner')


# 使用ModelSerializer类，create和update方法简单默认实现
# # 给定经过验证的数据，创建并返回新的Snippet实例
# def create(self, validated_data):
#     return Snippet.objects.create(**validated_data)
#
# # 给定经过验证的数据，更新并返回已经存在的Snippet
#
# def update(self, instance, validated_data):
#     instance.title = validated_data.get('title', instance.title)
#     instance.code = validated_data.get('code', instance.code)
#     instance.save()
#     return instance


# 添加用户模型序列化器
class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')
