from rest_framework.views import APIView
from rest_framework.views import Response
from rest_framework.views import Request
from rest_framework import status
from rest_framework import authentication, permissions

from django.shortcuts import get_object_or_404

from core.models import Person
from core.serializers import PersonSerializer


class PersonList(APIView):
    """
    List people or create a new person

    GET /person -> list people
    POST /person -> create a new cart person

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request: Request) -> Response:
        people = Person.objects.all()
        serializer = PersonSerializer(people, many=True)

        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = PersonSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonDetail(APIView):
    """
    Retrieve, update or delete a Person instance.

    GET /person/:id -> Get a person instance
    PUT /person/:id -> Updates a person instance
    DELETE /person/:id -> Deletes a person instance

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request: Request, pk: int) -> Response:
        person = get_object_or_404(Person, pk=pk)
        serializer = PersonSerializer(person)

        return Response(serializer.data)

    def put(self, request: Request, pk: int) -> Response:
        person = get_object_or_404(Person, pk=pk)
        serializer = PersonSerializer(person, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int) -> Response:
        person = get_object_or_404(Person, pk=pk)
        person.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
