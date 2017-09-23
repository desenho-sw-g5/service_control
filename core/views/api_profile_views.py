from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework.views import Request
from rest_framework import status
from rest_framework import authentication, permissions

from django.shortcuts import get_object_or_404

from core.models import Profile
from core.serializers import ProfileSerializer


class ProfileList(APIView):
    """
    List people or create a new profile

    GET /profile -> list profiles
    POST /profile -> create a new profile

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser, permissions.IsAuthenticated)

    def get(self, request: Request) -> Response:
        people = Profile.objects.all()
        serializer = ProfileSerializer(people, many=True)

        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetail(APIView):
    """
    Retrieve, update or delete a profile instance.

    GET /profile/:id/ -> Get a profile instance
    PATCH /profile/:id/ -> Updates a profile instance
    DELETE /profile/:id/ -> Deletes a profile instance

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser, permissions.IsAuthenticated)

    def get(self, request: Request, pk: int) -> Response:
        profile = get_object_or_404(Profile, pk=pk)
        serializer = ProfileSerializer(profile)

        return Response(serializer.data)

    def patch(self, request: Request, pk: int) -> Response:
        profile = get_object_or_404(Profile, pk=pk)

        serializer = ProfileSerializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int) -> Response:
        profile = get_object_or_404(Profile, pk=pk)
        profile.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
