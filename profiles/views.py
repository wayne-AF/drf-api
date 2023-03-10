from django.http import Http404
from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
# could use django's httpresponse but the response class is specifically built
# for the rest framework and provides a nicer interface for returning content-
# negotiated web api responses that can be rendered to multiple formats
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
# importing from permissions.py in drf_api folder
from drf_api.permissions import IsOwnerOrReadOnly


# class ProfileList(APIView):
#     """
#     List all profiles
#     No Create view (post method) as profile creation is handled by Django
#     signals
#     """
#     def get(self, request):
#         # returning all the profiles
#         profiles = Profile.objects.all()
#         # serialising all the profiles
#         serializer = ProfileSerializer(
#             # context part allows us to access request object from inside
#             # serializer
#             profiles, many=True, context={'request': request}
#             )
#         # sending serialised data in the response
#         return Response(serializer.data)


class ProfileList(generics.ListAPIView):
    """
    List all profiles
    No create view as profile creation is handled by django signals
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

# class ProfileDetail(APIView):

#     # makes it appear as a form?
#     serializer_class = ProfileSerializer
#     permission_classes = [IsOwnerOrReadOnly]

#     def get_object(self, pk):
#         try:
#             profile = Profile.objects.get(pk=pk)
#             # checking object permissions before returning profile instance
#             self.check_object_permissions(self.request, profile)
#             return profile
#         except Profile.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         profile = self.get_object(pk)
#         serializer = ProfileSerializer(
#             profile, context={'request': request}
#             )
#         return Response(serializer.data)

#     def put(self, request, pk):
#         profile = self.get_object(pk)
#         serializer = ProfileSerializer(
#             profile, data=request.data, context={'request': request}
#             )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        