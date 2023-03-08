from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer


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