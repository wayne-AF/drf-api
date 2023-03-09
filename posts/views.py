from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer
from drf_api.permissions import IsOwnerOrReadOnly
from django.http import Http404


class PostList(APIView):
    # makes it into a form
    serializer_class = PostSerializer

    # makes form disappear unless user is logged in
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get(self, request):
        # must retrieve all posts from database
        posts = Post.objects.all()
        # must serialize all posts
        serializer = PostSerializer(
            posts, many=True, context={'request': request}
        )
        # return serialized data in the response
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class PostDetail(APIView):

    serializer_class = PostSerializer
    # only post owner can edit or delete it
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            post = Post.objects.get(pk=pk)
            # checking if user has permission to edit the post
            self.check_object_permissions(self.request, post)
            return post
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        # handles post-doesn't-exist error
        post = self.get_object(pk)
        serializer = PostSerializer(
            post, context={'request': request}
        )
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(
            post, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
