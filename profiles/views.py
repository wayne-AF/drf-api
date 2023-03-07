from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
# could use django's httpresponse but the response class is specifically built for the rest framework and 
# provides a nicer interface for returning content-negotiated web api responses that can be
# rendered to multiple formats
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(APIView):
    """
    List all profiles
    No Create view (post method) as profile creation is handled by Django signals
    """
    def get(self, request):
        # returning all the profiles
        profiles = Profile.objects.all()
        # serialising all the profiles
        serializer = ProfileSerializer(profiles, many=True)
        # sending serialised data in the response
        return Response(serializer.data)


class ProfileDetail(APIView):
    serializer_class = ProfileSerializer
    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)