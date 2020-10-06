from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Events
from .serializer import EventSerializer, \
    FileSerializer, EventCreateUpdateSerializer


class EventCreateListView(generics.GenericAPIView,
                mixins.ListModelMixin,
                mixins.CreateModelMixin):

    queryset = Events.objects.all()
    lookup_field = 'id'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EventSerializer
        elif self.request.method == 'POST':
            return EventCreateUpdateSerializer

    def get(self, request, id=None, *args, **kwargs):
        return self.list(request)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class EventUpdateDeleteView(generics.GenericAPIView,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):

    queryset = Events.objects.all()
    lookup_field = 'id'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EventSerializer
        elif self.request.method == 'PUT':
            return EventCreateUpdateSerializer

    def get(self, request, id, *args, **kwargs):
        return self.retrieve(request, id)

    def put(self, request, id):
        try:
            return self.update(request, id)
        except Exception as e:
            print(e)

    def delete(self, request, id):
        return self.destroy(request, id)


class FileUploadView(APIView):

    def get(self, request, id=None, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class FileOnlyUploadView(APIView):

    parser_classes = [FileUploadParser]

    def get(self, request, id=None, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        print(request.data)
