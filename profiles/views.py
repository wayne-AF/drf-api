from django.shortcuts import render
from rest_framework.views import APIView
# could use django's httpresponse but the response class is specifically built for the rest framework and 
# provides a nicer interface for returning content-negotiated web api responses that can be
# rendered to multiple formats
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)

        return Response(serializer.data)
