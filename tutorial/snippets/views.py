from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer

# 基于函数的视图
# 基于函数的视图
# Create your views here.

# # @csrf_exempt
# @api_view(['GET', 'POST'])
# def snippet_list(request, format=None):
#     # 列出snippet或者创建snippet
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         # return JsonResponse(serializer.data, safe=False)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         # data = JSONParser().parse(request)
#         # serializer = SnippetSerializer(data=data)
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # return JsonResponse(serializer.data, status=201)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         # return JsonResponse(serializer.errors, status=400)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# # @csrf_exempt
# @api_view(['GET', 'POST', 'DELETE'])
# def snippet_detail(request, pk, format=None):
#     # 检查，更新或者删除
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         # return HttpResponse(status=404)
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         # return JsonResponse(serializer.data)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         # data = JSONParser().parse(request)
#         # serializer = SnippetSerializer(snippet, data=data)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # return JsonResponse(serializer.data)
#             return Response(serializer.data)
#         # return JsonResponse(serializer.errors, status=400)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         snippet.delete()
#         # return HttpResponse(status=204)
#         return Response(status=status.HTTP_204_NO_CONTENT)


# # 基于类的视图
# class SnippetList(APIView):
#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class SnippetDetail(APIView):
#     # 检查更新或者删除
#     def get_object(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             return Http404
#
#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# 基于mixins类
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics

#
# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# 基于generics
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics
from snippets.permissions import ISOwnerReadOnly


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # 权限判断
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # 这个perform_create() 可以让用户在通过POST请求创建一个
    # 新的Snippet时，在保存新的Snippet数据的时候
    # 会把request中的user赋值给Snippet的owner
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # 权限判断
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, ISOwnerReadOnly,)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
