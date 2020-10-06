from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser
from .serializer import UserSerializer, UserListSerializer, \
    UserCreateUpdateSerializer, LoginSerializer, LogoutSerializer


# Create your views here.
class UserView(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.filter(is_superuser=True).select_related('profile')

    # def get_queryset(self):
    #     querySet = User.objects.filter(is_superuser=True).select_related('profile')
    #     return querySet

    # def get(self,request,*args, **kwargs):
    #     return self.list(request,*args, **kwargs)



class ListPagination(PageNumberPagination):
    """
    Pagination List pagination
    """
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserCreateList(generics.GenericAPIView,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin):
    """
    User List View
    """
    # authentication_classes = (TokenAuthentication, )
    # permission_classes = (IsAuthenticated,)
    # pagination_class = ListPagination
    # serializer_class = UserListSerializer
    queryset = User.objects.all()
    lookup_field = 'id'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_staff','email']
    search_fields = ['profile__address']

    # def get_queryset(self):
    #     querySet = User.objects.filter(is_superuser=False).select_related('profile').prefetch_related('groups')
    #     return querySet


    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserListSerializer
        elif self.request.method == 'POST' or self.request.method == 'PUT':
            return UserCreateUpdateSerializer

    def get(self,request,id=None,*args,**kwargs):
        try:
            if id:
                return self.retrieve(request,*args,**kwargs)
            else:
                return self.list(request, *args, **kwargs)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self,request,*args,**kwargs):
        try:
            return self.create(request,*args,**kwargs)
        except Exception as e:
            print(e)
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            return self.update(request, *args, **kwargs)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Login(generics.GenericAPIView):
    """
    Login
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        try:
            self.serializer = self.get_serializer(data=request.data)
            if not self.serializer.is_valid():
                return Response(self.serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            credentials = {'email':request.data.get("email"),'password':request.data.get("password")}
            user_login = CustomUser().authenticate_user(**credentials)
            if user_login['status']:
                return Response({"data": {"token": user_login['token']}}, status=status.HTTP_200_OK)
            else:
                return Response({"message" : user_login['data']}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Logout(generics.GenericAPIView):
    """
    Logout
    """
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        try:
            self.serializer = self.get_serializer(data=request.data)
            if not self.serializer.is_valid():
                return Response(self.serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({"data": "logout"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
